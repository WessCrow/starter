#!/usr/bin/env python3
"""Validador de coerência de specs do STARTER.

Para cada diretório `specs/NNN-*/` (raiz e dentro de _lab/pilot-*/) verifica:
  (a) Cada critério de aceite de spec.md tem ≥1 task correspondente em tasks.md.
  (b) plan.md existe quando tasks.md existe (ordem de análise antes de execução).
  (c) tasks.md contém coluna ou seção de Verificação preenchida.

Uso:
  python3 skills/infra/scripts/check-spec-coherence.py [--strict]

Flags:
  --strict   Falha se qualquer spec não tiver plan.md (padrão: apenas aviso).

Saída:
  Imprime PASS/FAIL por spec e encerra com código 0 (tudo OK) ou 1 (algum FAIL).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[3]

# Locais onde procurar diretórios de spec
def _build_spec_roots() -> list[Path]:
    roots = [REPO_ROOT / "specs"]
    lab = REPO_ROOT / "_lab"
    if lab.is_dir():
        roots.extend(sorted(lab.glob("*/specs")))
    return roots


SPEC_ROOTS: list[Path] = _build_spec_roots()

_CRITERIA_SECTION_HEADERS = re.compile(
    r"^#{1,3}\s+(critérios?\s+de\s+aceite|acceptance\s+criteria)",
    re.IGNORECASE,
)
_CRITERION_LINE = re.compile(r"^\s*[-*]|\s*\d+\.")
_RISKS_SECTION_HEADERS = re.compile(
    r"^#{1,3}\s+(análise\s+de\s+riscos?|riscos?|risks?)",
    re.IGNORECASE,
)
_RISK_LINE = re.compile(r"^\s*[-*]\s+\*\*Risco:\*\*|^\s*[-*]\s+risk:", re.IGNORECASE)
_TASK_LINE = re.compile(
    r"^\|\s*\[[ xX]\]"  # tabela Markdown com checkbox
    r"|^\s*-\s*\[[ xX]\]"  # lista com checkbox
)
_VERIFICATION_COLUMN = re.compile(r"\|\s*verificação\s*\|", re.IGNORECASE)
_VERIFICATION_SECTION = re.compile(r"^#{1,4}\s+verificação", re.IGNORECASE)
_VERIFICATION_CELL_FILLED = re.compile(r"\|\s*[^|\s][^|]*\|")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _find_spec_dirs(
    strict: bool,
    spec_roots: list[Path] | None = None,
) -> list[Path]:
    """Retorna todos os diretórios de spec encontrados nas spec_roots (padrão: SPEC_ROOTS)."""
    roots = spec_roots if spec_roots is not None else SPEC_ROOTS
    dirs: list[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        for candidate in sorted(root.iterdir()):
            if candidate.is_dir() and re.match(r"^\d{3}-", candidate.name):
                dirs.append(candidate)
    return dirs


def _extract_criteria(spec_text: str) -> list[str]:
    """Extrai linhas de critérios de aceite do spec.md."""
    lines = spec_text.splitlines()
    in_section = False
    criteria: list[str] = []

    for line in lines:
        if _CRITERIA_SECTION_HEADERS.match(line):
            in_section = True
            continue
        if in_section:
            # Nova seção de nível equivalente ou maior encerra coleta
            if re.match(r"^#{1,3}\s+", line) and not _CRITERIA_SECTION_HEADERS.match(line):
                break
            if _CRITERION_LINE.match(line):
                text = line.strip().lstrip("-*0123456789. []xX").strip()
                if text:
                    criteria.append(text)

    return criteria


def _extract_risks(spec_text: str) -> list[str]:
    """Extrai linhas de riscos da seção Análise de Riscos do spec.md."""
    lines = spec_text.splitlines()
    in_section = False
    risks: list[str] = []

    for line in lines:
        if _RISKS_SECTION_HEADERS.match(line):
            in_section = True
            continue
        if in_section:
            if re.match(r"^#{1,3}\s+", line) and not _RISKS_SECTION_HEADERS.match(line):
                break
            if _RISK_LINE.match(line) or _RISK_LINE.match(line.lstrip()):
                text = line.strip()
                # Extrair o conteúdo após **Risco:** ou risk:
                if "**risco:**" in text.lower():
                    # Remover prefixo e o próprio Risco:
                    parts = re.split(r"\*\*risco:\*\*", text, flags=re.IGNORECASE)
                    text = parts[-1].strip()
                elif "risk:" in text.lower():
                    parts = re.split(r"risk:", text, flags=re.IGNORECASE)
                    text = parts[-1].strip()
                else:
                    text = text.lstrip("-* []")
                if text:
                    risks.append(text)

    return risks


def _count_tasks(tasks_text: str) -> int:
    """Conta linhas de tasks (com checkbox) em tasks.md."""
    return sum(1 for line in tasks_text.splitlines() if _TASK_LINE.match(line))


def _has_verification(tasks_text: str) -> bool:
    """Verifica se tasks.md contém coluna ou seção de Verificação preenchida."""
    lines = tasks_text.splitlines()

    # Verificar coluna de tabela
    has_column = any(_VERIFICATION_COLUMN.search(line) for line in lines)
    if has_column:
        # Exigir pelo menos uma célula preenchida abaixo do cabeçalho
        in_table = False
        for line in lines:
            if _VERIFICATION_COLUMN.search(line):
                in_table = True
                continue
            if in_table and line.startswith("|"):
                # Pular separador (|---|)
                if re.match(r"^\|[\s\-|]+\|$", line):
                    continue
                # Verificar se a última coluna tem conteúdo
                cells = [c.strip() for c in line.strip("|").split("|")]
                if cells and cells[-1] and cells[-1] not in ("-", "—", ""):
                    return True
        # Coluna existe mas todas as células vazias → falha
        return False

    # Verificar seção ## Verificação com conteúdo
    in_section = False
    for line in lines:
        if _VERIFICATION_SECTION.match(line):
            in_section = True
            continue
        if in_section:
            if re.match(r"^#{1,4}\s+", line):
                break
            if line.strip() and not line.strip().startswith("```"):
                return True  # tem conteúdo após o header

    return False


# ---------------------------------------------------------------------------
# Checks por spec dir
# ---------------------------------------------------------------------------

def _check_files_exist(spec_dir: Path) -> tuple[list[str], list[str]]:
    """Verifica existência dos arquivos obrigatórios."""
    passes: list[str] = []
    errors: list[str] = []

    for fname in ("spec.md",):
        if (spec_dir / fname).is_file():
            passes.append(f"{spec_dir.name}/{fname}: existe")
        else:
            errors.append(f"{spec_dir.name}/{fname}: AUSENTE (obrigatório)")

    return passes, errors


def _check_plan_before_tasks(spec_dir: Path, strict: bool) -> tuple[list[str], list[str]]:
    """(b) plan.md deve existir quando tasks.md existe."""
    passes: list[str] = []
    errors: list[str] = []

    has_plan = (spec_dir / "plan.md").is_file()
    has_tasks = (spec_dir / "tasks.md").is_file()

    if has_tasks and not has_plan:
        msg = f"{spec_dir.name}: tasks.md existe mas plan.md AUSENTE (análise antes de execução)"
        if strict:
            errors.append(msg)
        else:
            # Aviso leve — não falha o check
            passes.append(f"AVISO — {msg}")
    elif has_plan and has_tasks:
        passes.append(f"{spec_dir.name}: plan.md + tasks.md presentes")
    elif has_plan and not has_tasks:
        passes.append(f"{spec_dir.name}: plan.md presente, tasks.md ainda não criado (OK)")

    return passes, errors


def _check_criteria_coverage(spec_dir: Path) -> tuple[list[str], list[str]]:
    """(a) Cada critério de aceite do spec.md tem ≥1 task em tasks.md."""
    passes: list[str] = []
    errors: list[str] = []

    spec_path = spec_dir / "spec.md"
    tasks_path = spec_dir / "tasks.md"

    if not spec_path.is_file():
        return passes, errors  # já reportado em _check_files_exist

    spec_text = spec_path.read_text(encoding="utf-8")
    criteria = _extract_criteria(spec_text)

    # Filtrar placeholders
    valid_criteria = []
    for c in criteria:
        if "[ação]" in c or "[resultado]" in c or "[comportamento]" in c or "Ao , o usuário vê" in c:
            errors.append(f"{spec_dir.name}: critério de aceite contém placeholder não preenchido: '{c}'")
        else:
            valid_criteria.append(c)

    if not valid_criteria:
        errors.append(f"{spec_dir.name}: nenhum critério de aceite válido declarado em spec.md")
        return passes, errors

    if not tasks_path.is_file():
        errors.append(
            f"{spec_dir.name}: {len(valid_criteria)} critério(s) em spec.md mas tasks.md AUSENTE"
        )
        return passes, errors

    tasks_text = tasks_path.read_text(encoding="utf-8")
    n_tasks = _count_tasks(tasks_text)

    if n_tasks == 0:
        errors.append(
            f"{spec_dir.name}: {len(valid_criteria)} critério(s) em spec.md mas tasks.md não tem tasks com checkbox"
        )
    elif n_tasks < len(valid_criteria):
        errors.append(
            f"{spec_dir.name}: {len(valid_criteria)} critério(s) mas apenas {n_tasks} task(s) — cobertura insuficiente"
        )
    else:
        passes.append(
            f"{spec_dir.name}: {len(valid_criteria)} critério(s) cobertas por {n_tasks} task(s)"
        )

    return passes, errors


def _check_risks_analysis(spec_dir: Path) -> tuple[list[str], list[str]]:
    """Garante que a Análise de Riscos existe no spec.md e tem riscos válidos mapeados."""
    passes: list[str] = []
    errors: list[str] = []

    spec_path = spec_dir / "spec.md"
    if not spec_path.is_file():
        return passes, errors

    spec_text = spec_path.read_text(encoding="utf-8")
    
    # 1. Verificar se a seção existe
    has_section = any(_RISKS_SECTION_HEADERS.match(line) for line in spec_text.splitlines())
    if not has_section:
        errors.append(f"{spec_dir.name}: spec.md não contém a seção de 'Análise de Riscos'")
        return passes, errors

    risks = _extract_risks(spec_text)
    
    # 2. Verificar se existem riscos válidos e sem placeholders
    valid_risks = []
    for r in risks:
        if "[Descreva o risco" in r or "Vazamento de dados em sessão aberta" in r:
            errors.append(f"{spec_dir.name}: análise de riscos contém placeholder não preenchido: '{r}'")
        else:
            valid_risks.append(r)

    if not valid_risks:
        errors.append(f"{spec_dir.name}: nenhum risco válido com mitigação declarado em Análise de Riscos")
    else:
        passes.append(f"{spec_dir.name}: {len(valid_risks)} risco(s) e mitigação(ões) mapeados")

    return passes, errors


def _check_verification_filled(spec_dir: Path) -> tuple[list[str], list[str]]:
    """(c) tasks.md tem coluna ou seção Verificação preenchida."""
    passes: list[str] = []
    errors: list[str] = []

    tasks_path = spec_dir / "tasks.md"
    if not tasks_path.is_file():
        return passes, errors

    tasks_text = tasks_path.read_text(encoding="utf-8")
    n_tasks = _count_tasks(tasks_text)

    if n_tasks == 0:
        # Sem tasks → sem verificação necessária
        return passes, errors

    if _has_verification(tasks_text):
        passes.append(f"{spec_dir.name}: tasks.md tem Verificação preenchida")
    else:
        errors.append(
            f"{spec_dir.name}: tasks.md com {n_tasks} task(s) mas sem Verificação preenchida"
        )

    return passes, errors


# ---------------------------------------------------------------------------
# Runner principal
# ---------------------------------------------------------------------------

def check_spec_coherence(
    strict: bool = False,
    spec_roots: list[Path] | None = None,
) -> tuple[list[str], list[str]]:
    """Executa todos os checks em todos os spec dirs encontrados.

    Args:
        strict: Se True, falha quando plan.md ausente; padrão apenas avisa.
        spec_roots: Raízes de busca; usa SPEC_ROOTS do repositório se None.

    Returns:
        (passes, errors): listas de strings de resultado.
    """
    all_passes: list[str] = []
    all_errors: list[str] = []

    spec_dirs = _find_spec_dirs(strict, spec_roots=spec_roots)

    if not spec_dirs:
        all_passes.append("check-spec-coherence: nenhum diretório de spec encontrado (OK)")
        return all_passes, all_errors

    for spec_dir in spec_dirs:
        for check_fn in (
            _check_files_exist,
            lambda d: _check_plan_before_tasks(d, strict),
            _check_criteria_coverage,
            _check_risks_analysis,
            _check_verification_filled,
        ):
            p, e = check_fn(spec_dir)
            all_passes.extend(p)
            all_errors.extend(e)

    return all_passes, all_errors


def main() -> None:
    """Entry point para execução standalone."""
    strict = "--strict" in sys.argv

    passes, errors = check_spec_coherence(strict=strict)

    for msg in passes:
        prefix = "WARN" if msg.startswith("AVISO") else "OK  "
        print(f"{prefix} {msg}")
    for msg in errors:
        print(f"FAIL {msg}")

    total = len(passes) + len(errors)
    print(f"\n{total} checks, {len(errors)} falha(s)")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
