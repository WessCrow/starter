#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.error
import threading
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent
QUEUE_PATH = WORKSPACE_ROOT / "specs" / "queue.yaml"

def get_yaml_lib():
    try:
        import yaml
        return yaml
    except ImportError:
        print("\n[Erro] Biblioteca 'pyyaml' não encontrada no ambiente Python atual.")
        print("Para resolver, execute o script utilizando o ambiente virtual (.venv) do projeto:")
        print("  .venv/bin/python3 skills/scripts/run_parallel_agents.py")
        print("Ou ative o ambiente virtual antes de rodar:")
        print("  source .venv/bin/activate && python3 skills/scripts/run_parallel_agents.py\n")
        sys.exit(1)

def call_gemini_api(api_key: str, prompt: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as res:
            response_data = json.loads(res.read().decode("utf-8"))
            candidates = response_data.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts:
                    return parts[0].get("text", "")
            raise Exception("API retornou resposta sem texto válido.")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise Exception(f"HTTP Error {e.code}: {error_body}")

def call_claude_api(api_key: str, prompt: str) -> str:
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    body = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 4096,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as res:
            response_data = json.loads(res.read().decode("utf-8"))
            content = response_data.get("content", [])
            if content:
                return content[0].get("text", "")
            raise Exception("API retornou resposta vazia.")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise Exception(f"HTTP Error {e.code}: {error_body}")

def run_task(task_data: dict, yaml):
    task_id = task_data.get("id")
    task_desc = task_data.get("task")
    target_file_rel = task_data.get("target_file")
    context_files_rel = task_data.get("context_files", [])
    
    print(f"[Agente-{task_id}] Processando: {task_desc}")
    
    try:
        # 1. Carregar chaves de API
        # Tenta carregar do .env local se existir
        env_path = WORKSPACE_ROOT / ".env"
        api_keys = {}
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    api_keys[k.strip()] = v.strip()
                    
        gemini_key = os.environ.get("GEMINI_API_KEY") or api_keys.get("GEMINI_API_KEY")
        claude_key = os.environ.get("ANTHROPIC_API_KEY") or api_keys.get("ANTHROPIC_API_KEY")
        
        # 2. Carregar contexto dos arquivos
        context_str = ""
        for rel_path in context_files_rel:
            p = WORKSPACE_ROOT / rel_path
            if p.exists() and p.is_file():
                context_str += f"=== CONTEÚDO DO ARQUIVO: {rel_path} ===\n"
                context_str += p.read_text(encoding="utf-8", errors="ignore")
                context_str += "\n====================================\n\n"
                
        # 3. Montar o Prompt do Agente
        system_prompt = (
            "Você é um agente de desenvolvimento de IA especializado e autônomo.\n"
            "Sua tarefa é modificar ou criar o arquivo especificado de acordo com as instruções.\n"
            "REGRAS DE RETORNO:\n"
            "- Retorne EXCLUSIVAMENTE o conteúdo textual/código completo que deve ser escrito no arquivo de destino.\n"
            "- NÃO adicione cercas de código markdown (como ```python ou ```), comentários explicativos fora do código ou prefácios.\n"
            "- Seu output será gravado diretamente no arquivo de destino.\n\n"
        )
        
        full_prompt = (
            f"{system_prompt}"
            f"{context_str}"
            f"Instrução: {task_desc}\n"
            f"Arquivo de Destino: {target_file_rel}\n"
        )
        
        # 4. Chamar o modelo disponível
        if gemini_key:
            response_code = call_gemini_api(gemini_key, full_prompt)
        elif claude_key:
            response_code = call_claude_api(claude_key, full_prompt)
        else:
            raise Exception("API Keys ausentes. Por favor, configure GEMINI_API_KEY ou ANTHROPIC_API_KEY nas variáveis de ambiente ou em um arquivo .env na raiz do projeto.")
            
        # 5. Tratar limpeza básica de markdown no código se o modelo falhar nas regras
        lines = response_code.strip().splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned_code = "\n".join(lines)
        
        # 6. Gravar o arquivo de destino
        target_path = WORKSPACE_ROOT / target_file_rel
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(cleaned_code, encoding="utf-8")
        
        # 7. Atualizar status na fila
        task_data["status"] = "success"
        task_data["error"] = None
        print(f"[Agente-{task_id}] Sucesso! Código gravado em: {target_file_rel}")
        
    except Exception as e:
        task_data["status"] = "failed"
        task_data["error"] = str(e)
        print(f"[Agente-{task_id}] Erro: {e}")

def main():
    yaml = get_yaml_lib()
    
    if not QUEUE_PATH.exists():
        print(f"Fila de tarefas {QUEUE_PATH} não encontrada.")
        sys.exit(0)
        
    with open(QUEUE_PATH, "r", encoding="utf-8") as f:
        queue_data = yaml.safe_load(f) or {}
        
    tasks = queue_data.get("queue", [])
    if not tasks:
        print("Nenhuma tarefa pendente na fila.")
        sys.exit(0)
        
    threads = []
    has_changes = False
    
    for task in tasks:
        if task.get("status") == "pending":
            task["status"] = "running"
            has_changes = True
            
            # Executa a tarefa em uma thread paralela
            t = threading.Thread(target=run_task, args=(task, yaml))
            t.start()
            threads.append(t)
            
    if has_changes:
        # Gravar status intermediário "running"
        with open(QUEUE_PATH, "w", encoding="utf-8") as f:
            yaml.safe_dump(queue_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            
        # Aguardar todas as threads terminarem
        for t in threads:
            t.join()
            
        # Gravar resultados finais na fila
        with open(QUEUE_PATH, "w", encoding="utf-8") as f:
            yaml.safe_dump(queue_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            
        print("Todas as tarefas paralelas da fila foram processadas.")

if __name__ == "__main__":
    main()
