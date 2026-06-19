#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent
RUNTIME_DIR = WORKSPACE_ROOT / "skills" / "core" / "runtime"
STATE_PATH = RUNTIME_DIR / "state.yaml"
REPORTS_DIR = WORKSPACE_ROOT / "qa" / "reports"

# Máximo de tentativas falhas por comando para evitar loop infinito
MAX_FAILURES = 3

def get_yaml_lib():
    try:
        import yaml
        return yaml
    except ImportError:
        print("Erro: biblioteca pyyaml não encontrada. Por favor, execute no ambiente com dependências.")
        sys.exit(1)

def run_cmd(cmd_str: str, cmd_id: str) -> tuple[int, Path]:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    log_path = REPORTS_DIR / f"daemon_{cmd_id}.log"
    
    print(f"[{datetime.datetime.now().isoformat()}] Executando: {cmd_str}")
    
    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"=== DAEMON EXECUTION LOG ===\n")
        log_file.write(f"Command: {cmd_str}\n")
        log_file.write(f"Started At: {datetime.datetime.now().isoformat()}\n")
        log_file.write(f"============================\n\n")
        log_file.flush()
        
        # Executa o comando local
        result = subprocess.run(
            cmd_str,
            shell=True,
            stdout=log_file,
            stderr=log_file,
            cwd=str(WORKSPACE_ROOT),
            text=True
        )
        
        log_file.write(f"\n============================\n")
        log_file.write(f"Finished At: {datetime.datetime.now().isoformat()}\n")
        log_file.write(f"Exit Code: {result.returncode}\n")
        
    return result.returncode, log_path

def main():
    yaml = get_yaml_lib()
    
    print(f"STARTER Daemon Watcher ativo monitorando: {STATE_PATH}")
    print("Pressione Ctrl+C para encerrar.")
    
    failure_counters = {}
    
    while True:
        try:
            if not STATE_PATH.exists():
                time.sleep(1)
                continue
                
            # Ler state.yaml
            with open(STATE_PATH, "r", encoding="utf-8") as f:
                try:
                    state_data = yaml.safe_load(f) or {}
                except Exception:
                    # Se o arquivo estiver sendo gravado ao mesmo tempo, pode dar erro de parse.
                    # Aguardar e tentar novamente.
                    time.sleep(0.5)
                    continue
            
            daemon_section = state_data.get("daemon", {})
            commands = daemon_section.get("commands", [])
            
            if not commands:
                time.sleep(1)
                continue
                
            has_changes = False
            for cmd in commands:
                if cmd.get("status") == "pending":
                    cmd_id = cmd.get("id")
                    cmd_str = cmd.get("cmd")
                    
                    # Evitar loop de erro
                    fail_count = failure_counters.get(cmd_id, 0)
                    if fail_count >= MAX_FAILURES:
                        print(f"Aviso: Comando {cmd_id} atingiu limite de falhas. Ignorando.")
                        cmd["status"] = "failed"
                        cmd["exit_code"] = -999
                        cmd["log_path"] = ""
                        has_changes = True
                        continue
                    
                    # Atualiza status para rodando e grava no arquivo
                    cmd["status"] = "running"
                    with open(STATE_PATH, "w", encoding="utf-8") as f:
                        yaml.safe_dump(state_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
                    
                    # Executa
                    exit_code, log_path = run_cmd(cmd_str, cmd_id)
                    
                    # Relativiza o log path para salvar no yaml de forma limpa
                    rel_log_path = str(log_path.relative_to(WORKSPACE_ROOT))
                    
                    # Atualiza com o resultado
                    cmd["status"] = "success" if exit_code == 0 else "failed"
                    cmd["exit_code"] = exit_code
                    cmd["log_path"] = rel_log_path
                    
                    if exit_code != 0:
                        failure_counters[cmd_id] = fail_count + 1
                        
                    has_changes = True
                    break # Executa um comando por vez por ciclo
            
            if has_changes:
                # Gravar de volta no arquivo
                with open(STATE_PATH, "w", encoding="utf-8") as f:
                    yaml.safe_dump(state_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
                print(f"[{datetime.datetime.now().isoformat()}] Estado de execução gravado em state.yaml")
                
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\nDaemon Watcher encerrado.")
            break
        except Exception as e:
            print(f"Erro no loop do daemon: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
