#!/usr/bin/env python3
import sys
import datetime
from pathlib import Path

# Adiciona o diretório do script para imports relativos se houver
SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent
RUNTIME_DIR = WORKSPACE_ROOT / "skills" / "core" / "runtime"
HANDOFF_PATH = RUNTIME_DIR / "handoff.yaml"

def get_token_count(text: str) -> tuple[int, str]:
    try:
        import tiktoken
        # Usamos cl100k_base (padrão GPT-4 e Gemini)
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text)), "tiktoken (cl100k_base)"
    except ImportError:
        # Fallback matemático do STARTER: 1 token ≈ 4 caracteres
        if not text:
            return 0, "fallback (1 token ≈ 4 caracteres)"
        return max(1, len(text) // 4), "fallback (1 token ≈ 4 caracteres)"

def main():
    try:
        import yaml
    except ImportError:
        print("Erro: biblioteca pyyaml não encontrada. Por favor, execute no ambiente virtual com as dependências.")
        sys.exit(1)

    if not HANDOFF_PATH.exists():
        print(f"Erro: {HANDOFF_PATH} não encontrado.")
        sys.exit(1)

    # 1. Mapear arquivos que fazem parte da janela de contexto do agente
    files_to_scan = []
    
    # Arquivos base na raiz
    for base_file in ["AGENTS.md", "README.md", "COMECAR-PROJETO.md"]:
        path = WORKSPACE_ROOT / base_file
        if path.exists() and path.is_file():
            files_to_scan.append(path)
            
    # Arquivos do Runtime
    if RUNTIME_DIR.exists():
        for f in RUNTIME_DIR.glob("*.yaml"):
            files_to_scan.append(f)
            
    # Arquivos de Fluxos
    flows_dir = WORKSPACE_ROOT / "skills" / "flows"
    if flows_dir.exists():
        for f in flows_dir.glob("*.md"):
            files_to_scan.append(f)
            
    # Arquivos do Catálogo de Skills
    catalog_dir = WORKSPACE_ROOT / "skills" / "catalog"
    if catalog_dir.exists():
        for f in catalog_dir.glob("*.skill"):
            files_to_scan.append(f)

    # Adiciona a feature ativa se houver
    with open(HANDOFF_PATH, "r", encoding="utf-8") as f:
        handoff_data = yaml.safe_load(f) or {}

    feature_data = handoff_data.get("feature", {})
    feature_id = feature_data.get("id")
    if feature_id:
        specs_dir = WORKSPACE_ROOT / "specs" / feature_id
        if specs_dir.exists() and specs_dir.is_dir():
            for f in specs_dir.glob("*"):
                if f.is_file() and f.suffix in [".md", ".ts", ".yaml", ".json"]:
                    files_to_scan.append(f)

    # Remover duplicatas mantendo a ordem e filtrar apenas arquivos existentes
    unique_files = []
    for f in files_to_scan:
        if f.exists() and f.is_file() and f not in unique_files:
            unique_files.append(f)

    # 2. Calcular tokens
    total_tokens = 0
    loaded_files_rel = []
    method_used = "fallback (1 token ≈ 4 caracteres)"

    for file_path in unique_files:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            tokens, method = get_token_count(content)
            total_tokens += tokens
            method_used = method  # Fica com o último método ou tiktoken se funcionar
            loaded_files_rel.append(str(file_path.relative_to(WORKSPACE_ROOT)))
        except Exception as e:
            print(f"Aviso: erro ao ler {file_path}: {e}")

    # 3. Atualizar handoff.yaml
    TETO_OTIMIZADO_TOKENS = 35000
    limit_exceeded = total_tokens > TETO_OTIMIZADO_TOKENS

    metrics = {
        "last_session_at": datetime.date.today().isoformat(),
        "files_loaded": sorted(loaded_files_rel),
        "files_loaded_count": len(loaded_files_rel),
        "estimated_tokens": total_tokens,
        "context_limit_exceeded": limit_exceeded,
        "unnecessary_files": [],
        "estimation_method": method_used
    }

    handoff_data["context_metrics"] = metrics
    handoff_data["updated"] = datetime.date.today().isoformat()

    with open(HANDOFF_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(handoff_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"Sucesso: handoff.yaml atualizado com {len(loaded_files_rel)} arquivos e {total_tokens} tokens usando o método: {method_used}")
    
    if limit_exceeded:
        print(f"\n[AVISO DE CONTEXTO] Contexto estimado ({total_tokens} tokens) excedeu o limite recomendado de {TETO_OTIMIZADO_TOKENS} tokens.")
        print("Sugere-se executar a skill 'context-cleaner.skill' para arquivar/resumir arquivos desnecessários.")

if __name__ == "__main__":
    main()
