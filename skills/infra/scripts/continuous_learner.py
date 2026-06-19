#!/usr/bin/env python3
"""
STARTER Continuous Learner — v1.0.0
Analyzes session logs (Loop 1) and compares them with subsequent human commits/changes
to detect overrides and suggest modifications to local skills.
"""
from __future__ import annotations

import os
import json
import sys
import subprocess
import datetime
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parents[3]
RUNS_DIR = REPO_ROOT / "qa" / "runs"
SKILLS_DIR = REPO_ROOT / "skills"
LOCAL_SKILLS_DIR = SKILLS_DIR / "catalog"
VALIDATOR = SKILLS_DIR / "infra" / "scripts" / "validate-skills.py"

def run_cmd(args: list[str]) -> tuple[int, str]:
    """Runs a shell command and returns status and output."""
    try:
        res = subprocess.run(args, cwd=REPO_ROOT, capture_output=True, text=True, check=False)
        return res.returncode, res.stdout + res.stderr
    except Exception as e:
        return -1, str(e)

def get_latest_trace() -> Path | None:
    """Finds the most recent session trace file in qa/runs/."""
    if not RUNS_DIR.exists():
        return None
    traces = list(RUNS_DIR.glob("session_*.json"))
    if not traces:
        return None
    # Sort by filename which contains date_time string
    traces.sort(key=lambda p: p.name, reverse=True)
    return traces[0]

def analyze_changes_for_file(filepath: str, since_iso: str) -> list[str]:
    """Retrieves commits touching this file since the trace timestamp."""
    # Convert ISO timestamp to UTC/Local format git accepts
    # Git log --since accepts ISO-8601
    code, out = run_cmd(["git", "log", f"--since={since_iso}", "--oneline", "--", filepath])
    if code == 0:
        return [line.strip() for line in out.splitlines() if line.strip()]
    return []

def main():
    print("--- INICIANDO CONTINUOUS LEARNER (LOOP 2) ---")
    
    trace_path = get_latest_trace()
    if not trace_path:
        print("Nenhum trace de sessão encontrado em qa/runs/.")
        sys.exit(0)
        
    print(f"Analisando trace mais recente: {trace_path.name}")
    with trace_path.open(encoding="utf-8") as f:
        trace = json.load(f)
        
    trace_time = trace.get("timestamp")
    files_touched = trace.get("files_touched", [])
    feature_id = trace.get("feature_id", "indefinida")
    
    print(f"Sessão gravada em: {trace_time}")
    print(f"Arquivos tocados na sessão: {files_touched}")
    
    overrides_detected = {}
    for fpath in files_touched:
        # Check git logs for this file since trace time
        commits = analyze_changes_for_file(fpath, trace_time)
        # Also check if the file currently has uncommitted changes that are different from the trace
        # (meaning the human is editing them right now)
        code, status_out = run_cmd(["git", "status", "--porcelain", "--", fpath])
        has_uncommitted = len(status_out.strip()) > 0
        
        if commits or has_uncommitted:
            overrides_detected[fpath] = {
                "commits": commits,
                "has_uncommitted_changes": has_uncommitted
            }
            
    if not overrides_detected:
        print("\n✅ Sucesso: Nenhum desalinhamento ou correção humana pós-sessão foi detectado.")
        print("O agente operou em perfeita harmonia com o desenvolvedor.")
        sys.exit(0)
        
    print("\n⚠️ DESALINHAMENTOS DETECTADOS (HUMAN OVERRIDES):")
    for fpath, details in overrides_detected.items():
        print(f"\n📂 Arquivo: {fpath}")
        if details["commits"]:
            print("  Commits posteriores:")
            for c in details["commits"]:
                print(f"    - {c}")
        if details["has_uncommitted_changes"]:
            print("  [Alerta] Existem modificações locais não commitadas neste arquivo.")
            
    # Propose which skills should be updated
    print("\n🔮 Sugestões de Aprendizado Contínuo:")
    print("--------------------------------------------------")
    
    # Simple heuristics to suggest which skill to refine
    for fpath in overrides_detected.keys():
        if fpath.endswith(".py"):
            print(f"- Sugestão: Adicionar validações de código ou testes extras em `skills/catalog/best-practices.skill`")
        elif fpath.endswith(".css") or "style" in fpath:
            print(f"- Sugestão: Refinar regras de Design Tokens semânticos em `skills/catalog/fluid-ui.skill` ou `skills/catalog/accessibility.skill`")
        elif "skill" in fpath or fpath.endswith(".skill"):
            print(f"- Sugestão: O próprio arquivo de habilidades foi modificado pelo humano. Sugere-se atualizar o log TDD de `{Path(fpath).name}`")
            
    print("\n[Intent Preview] Para aplicar estas melhorias autonomamente, selecione a skill alvo e adicione a regra sob o portão de validação.")
    print("Execute 'python3 skills/infra/scripts/validate-skills.py' após editar as skills.")

if __name__ == "__main__":
    main()
