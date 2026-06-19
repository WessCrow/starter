#!/usr/bin/env python3
"""
STARTER Independent QA Verifier — v5.5.0
Automates the independent QA verification step. Checks for:
- Code style & rules (Host Guard, console.log, ts_any, css_important)
- Repository hygiene (via check-repo-hygiene.py)
- Coherence of specs/tasks (via check-spec-coherence.py)
- Code compilation/tests (pnpm/npm build/lint/test)
- Unbiased LLM-based audit of code changes vs sprint-contract (optional, via API key)
Produces a QA report in qa/reports/.
"""
from __future__ import annotations

import os
import re
import sys
import json
import urllib.request
import subprocess
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parents[3]
RUNTIME_DIR = REPO_ROOT / "skills" / "core" / "runtime"

def load_yaml(path: Path) -> dict:
    """Helper to load a YAML file. Simple fallback to avoid dependency if possible."""
    try:
        import yaml
        with path.open(encoding="utf-8") as f:
            return yaml.safe_load(f)
    except ImportError:
        # Simple regex parser for basic yaml properties if pyyaml isn't available
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
                    if v.lower() == "true":
                        v = True
                    elif v.lower() == "false":
                        v = False
                    elif v.lower() == "null":
                        v = None
                    data[k] = v
        return data

def run_cmd(args: list[str], cwd: Path = REPO_ROOT) -> tuple[int, str]:
    """Runs a shell command and returns status and output."""
    try:
        res = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)
        return res.returncode, res.stdout + res.stderr
    except FileNotFoundError:
        return -1, "Command not found"

def check_rules_violations(diff_text: str) -> list[str]:
    """Checks the diff text for rules violations."""
    violations = []
    # Search for console.log
    if re.search(r"\+.*console\.log\b", diff_text):
        violations.append("Adição de console.log detectada (regra code.never.console_log)")
    # Search for TS 'any'
    if re.search(r"\+\s*.*:\s*any\b", diff_text) or re.search(r"\+.*as\s+any\b", diff_text):
        violations.append("Adição do tipo 'any' em TypeScript detectada (regra code.never.ts_any)")
    # Search for CSS !important
    if re.search(r"\+.*!important\b", diff_text):
        violations.append("Adição de CSS !important detectada (regra code.never.css_important)")
    return violations

def get_llm_audit(contract_text: str, diff_text: str) -> str:
    """Invokes LLM API (Gemini or Anthropic) if keys are present for an unbiased audit."""
    gemini_key = os.environ.get("GEMINI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    
    prompt = (
        "Você é um Auditor de QA independente e sético no framework STARTER.\n"
        "Seu objetivo é analisar as modificações de código (Git Diff) e compará-las com o contrato de entrega (Sprint Contract).\n"
        "Aponte falhas de lógica, regras violadas ou critérios de aceite não cumpridos.\n"
        "Retorne em formato markdown com as seguintes seções:\n"
        "- **Análise do Diferencial**: Quais arquivos foram alterados e se correspondem ao contrato.\n"
        "- **Avaliação dos Critérios**: Liste se os critérios do contrato foram atendidos, falharam ou não foram alterados.\n"
        "- **Veredito do Auditor**: PASS ou FAIL.\n\n"
        f"=== CONTRATO DA SPRINT ===\n{contract_text}\n\n"
        f"=== GIT DIFF ===\n{diff_text}\n"
    )

    if gemini_key:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=30) as res:
                response = json.loads(res.read().decode("utf-8"))
                return response["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"Erro na chamada do Gemini API: {e}"
            
    elif anthropic_key:
        url = "https://api.anthropic.com/v1/messages"
        payload = {
            "model": "claude-3-5-haiku-20241022",
            "max_tokens": 2048,
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "x-api-key": anthropic_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(req, timeout=30) as res:
                response = json.loads(res.read().decode("utf-8"))
                return response["content"][0]["text"]
        except Exception as e:
            return f"Erro na chamada do Anthropic API: {e}"

    return "Auditoria de LLM externa não configurada (variáveis GEMINI_API_KEY ou ANTHROPIC_API_KEY ausentes)."

def main():
    print("--- INICIANDO VERIFICADOR QA INDEPENDENTE ---")
    
    # Load settings
    qa_conf = load_yaml(RUNTIME_DIR / "qa.yaml")
    handoff = load_yaml(RUNTIME_DIR / "handoff.yaml")
    
    # 1. Locate Contract
    feature_id = handoff.get("feature", {}).get("id", "feature-indefinida")
    contract_path_str = handoff.get("feature", {}).get("sprint_contract_path", "sprint-contract.md")
    contract_path = REPO_ROOT / contract_path_str
    
    if not contract_path.is_file():
        contract_path = REPO_ROOT / "sprint-contract.md"
        
    contract_text = ""
    if contract_path.is_file():
        contract_text = contract_path.read_text(encoding="utf-8")
        print(f"Contrato localizado: {contract_path.name}")
    else:
        print("AVISO: sprint-contract.md não localizado no workspace.")

    # 2. Get git modifications
    # Diff against HEAD~1 or staged changes
    status_code, diff_cached = run_cmd(["git", "diff", "--cached"])
    status_code, diff_unstaged = run_cmd(["git", "diff"])
    diff_text = diff_cached + "\n" + diff_unstaged
    
    if not diff_text.strip():
        # Fallback: check changes in the last commit
        _, diff_text = run_cmd(["git", "diff", "HEAD~1", "HEAD"])
        print("Usando diff do último commit (nenhuma alteração pendente/staged).")
    else:
        print("Usando diff das modificações locais ativas.")

    # 3. Check for rule violations
    violations = check_rules_violations(diff_text)
    for v in violations:
        print(f"VIOLAÇÃO DE REGRA: {v}")

    # 4. Run Smoke Commands / Validations
    smoke_results = []
    
    # Python checks (Framework defaults)
    validate_code, validate_out = run_cmd(["python3", "skills/core/runtime/validate.py"])
    smoke_results.append(("validate.py", validate_code == 0, validate_out))
    
    hygiene_code, hygiene_out = run_cmd(["python3", "skills/infra/scripts/check-repo-hygiene.py"])
    smoke_results.append(("check-repo-hygiene.py", hygiene_code == 0, hygiene_out))
    
    coherence_code, coherence_out = run_cmd(["python3", "skills/infra/scripts/check-spec-coherence.py"])
    smoke_results.append(("check-spec-coherence.py", coherence_code == 0, coherence_out))
    
    # If package.json exists in workspace, run Node build/test
    if (REPO_ROOT / "package.json").is_file():
        print("Projeto Node detectado, executando smoke commands...")
        # Check package manager (pnpm vs npm)
        pkg_manager = "pnpm" if (REPO_ROOT / "pnpm-lock.yaml").is_file() else "npm"
        
        build_code, build_out = run_cmd([pkg_manager, "run", "build"])
        smoke_results.append((f"{pkg_manager} run build", build_code == 0, build_out))
        
        # Check if tests exist in package.json
        with (REPO_ROOT / "package.json").open() as f:
            package_data = json.load(f)
        if "test" in package_data.get("scripts", {}):
            test_code, test_out = run_cmd([pkg_manager, "run", "test"])
            smoke_results.append((f"{pkg_manager} run test", test_code == 0, test_out))

    # Determine status
    failures = [name for name, passed, _ in smoke_results if not passed] or violations
    final_status = "FAIL" if failures else "PASS"
    print(f"Status da auditoria local: {final_status}")

    # 5. Get LLM audit if configured
    llm_audit_report = get_llm_audit(contract_text, diff_text)

    # 6. Generate Report Markdown
    import datetime
    today = datetime.date.today().isoformat()
    report_name = f"{today}-{feature_id}.md"
    report_dir = REPO_ROOT / "qa" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / report_name

    # Build report output
    build_smoke_log = ""
    for name, passed, out in smoke_results:
        status_symbol = "OK" if passed else "FAIL"
        build_smoke_log += f"$ {name} -> {status_symbol}\n"
        # Truncate output if too long
        lines = out.splitlines()
        if len(lines) > 20:
            build_smoke_log += "\n".join(lines[:10]) + "\n... [TRUNCATED] ...\n" + "\n".join(lines[-10:])
        else:
            build_smoke_log += out
        build_smoke_log += "\n\n"

    report_content = f"""# Relatório QA Independente — {feature_id} — {today}

> **Status final:** {final_status}  
> **Idioma:** português simples

---

## Resumo (1 parágrafo)

Auditoria independente e sética realizada no código da feature `{feature_id}`. A validação mecânica de compilação, regras de código do repositório (Host Guard/higiene/coerência) resultou em **{final_status}**.

---

## Violamentos e Falhas de Regra

"""
    if violations:
        for v in violations:
            report_content += f"- **FAIL**: {v}\n"
    else:
        report_content += "- *Nenhuma violação de regras encontrada.*\n"

    report_content += f"""
---

## Auditoria Cognitiva Externa (LLM)

{llm_audit_report}

---

## Build / Terminal

```txt
{build_smoke_log}
```

---

## Próximo passo

"""
    if final_status == "FAIL":
        report_content += "- [ ] Corrigir itens apontados como FAIL e rodar o QA independente novamente.\n"
    else:
        report_content += "- [ ] PASS → usuário executa teste manual no navegador (5 min) → marcar concluído.\n"

    report_content += f"""
---

*Gerado automaticamente pelo script independent-qa.py (v5.5.0)*
"""

    report_path.write_text(report_content, encoding="utf-8")
    print(f"Relatório de QA independente gravado em: {report_path.relative_to(REPO_ROOT)}")
    
    # Print clean summary for Orchestrator to parse
    if final_status == "FAIL":
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
