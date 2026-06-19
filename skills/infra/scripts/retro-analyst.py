#!/usr/bin/env python3
"""
STARTER RetroAnalyst — v5.5.0
Analyzes session logs, git history, and QA reports to generate a retrospective report in docs/private/retrospectives/.
"""
from __future__ import annotations

import re
import sys
import datetime
import subprocess
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parents[3]
RUNTIME_DIR = REPO_ROOT / "skills" / "core" / "runtime"
RETRO_DIR = REPO_ROOT / "docs" / "private" / "retrospectives"

def load_yaml(path: Path) -> dict:
    """Helper to load a YAML file. Simple fallback to avoid dependency if possible."""
    try:
        import yaml
        with path.open(encoding="utf-8") as f:
            return yaml.safe_load(f)
    except ImportError:
        data = {}
        with path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    k, v = line.split(":", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    data[k] = v
        return data

def run_cmd(args: list[str]) -> tuple[int, str]:
    """Runs a shell command and returns status and output."""
    try:
        res = subprocess.run(args, cwd=REPO_ROOT, capture_output=True, text=True, check=False)
        return res.returncode, res.stdout + res.stderr
    except FileNotFoundError:
        return -1, "Command not found"

def analyze_git_history() -> list[str]:
    """Retrieves recent git commit messages to identify modifications."""
    code, out = run_cmd(["git", "log", "-n", "5", "--oneline"])
    if code == 0:
        return [line.strip() for line in out.splitlines() if line.strip()]
    return []

def main():
    print("--- INICIANDO RETROANALYST ---")
    
    # Load Handoff
    handoff = load_yaml(RUNTIME_DIR / "handoff.yaml")
    feature_id = handoff.get("feature", {}).get("id", "sprint-indefinida")
    
    # Analyze git commits
    commits = analyze_git_history()
    
    # Heuristics & Recommendations
    recommendations = []
    
    # Check if there are console.log, ts_any, css_important in rules.yaml
    rules = load_yaml(RUNTIME_DIR / "rules.yaml")
    
    # Check for recent file changes
    code, files_changed_str = run_cmd(["git", "diff", "--name-only", "HEAD~3"])
    files_changed = [line.strip() for line in files_changed_str.splitlines() if line.strip()]
    
    # Generate recommendations based on touched files
    has_js_ts = any(f.endswith((".js", ".jsx", ".ts", ".tsx")) for f in files_changed)
    has_css = any(f.endswith(".css") for f in files_changed)
    
    if has_js_ts:
        recommendations.append(
            "- **TypeScript/JavaScript:** Garantir que o linter local (`pnpm run lint` ou `npm run lint`) "
            "seja executado em ganchos de pré-commit para evitar erros de compilação remotos."
        )
    if has_css:
        recommendations.append(
            "- **Styling (CSS):** Validar se os novos estilos utilizam exclusivamente tokens semânticos "
            "definidos no design system, evitando cores/spacing hard-coded."
        )
        
    if not recommendations:
        recommendations.append("- *Nenhuma recomendação de melhoria encontrada para esta sessão.*")

    # Generate MD Content
    today = datetime.date.today().isoformat()
    RETRO_DIR.mkdir(parents=True, exist_ok=True)
    report_path = RETRO_DIR / f"{today}-{feature_id}.md"
    
    commits_md = "\n".join(f"- {c}" for c in commits) if commits else "- *Nenhum commit recente encontrado.*"
    files_md = "\n".join(f"- `{f}`" for f in files_changed[:10]) or "- *Nenhum arquivo modificado recentemente.*"
    if len(files_changed) > 10:
        files_md += f"\n- *... e mais {len(files_changed) - 10} arquivo(s).*"

    recommendations_md = "\n".join(recommendations)

    content = f"""# Retrospectiva de Sessão — {feature_id} — {today}

> **Tipo:** Análise pós-sprint retrospectiva  
> **Objetivo:** Identificar melhorias de regras e DX

---

## Histórico de Atividade Recente

### Commits analisados:
{commits_md}

### Arquivos modificados:
{files_md}

---

## Recomendações de Evolução do Framework (rules.yaml)

{recommendations_md}

---

*Gerado automaticamente pelo RetroAnalyst (v5.5.0)*
"""

    report_path.write_text(content, encoding="utf-8")
    print(f"Retrospectiva gravada com sucesso em: {report_path.relative_to(REPO_ROOT)}")

if __name__ == "__main__":
    main()
