#!/usr/bin/env python3
"""
STARTER System Validator.

Valida antidrift entre filesystem, docs centrais, templates, outputs e bootstrap.

Uso:
  python3 skills/scripts/validate-skills.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "skills"
GOVERNANCE_DIR = SKILLS_DIR / "governance"

LOCAL_DIR = SKILLS_DIR / "local-skills"
STRUCTURE_DIR = SKILLS_DIR / "structure"
DEFERRED_DIR = SKILLS_DIR / "_deferred"
LINKED_DIR = SKILLS_DIR / "linked-skills"
CACHE_DIR = SKILLS_DIR / "cache"
TEMPLATES_DIR = SKILLS_DIR / "templates"
OUTPUTS_DIR = SKILLS_DIR / "outputs"
RUNTIME_DIR = SKILLS_DIR / "runtime"
TEMPLATE_RUNTIME_DIR = TEMPLATES_DIR / "runtime"

START_MD = GOVERNANCE_DIR / "Start.md"
README_MD = SKILLS_DIR / "README.md"
INDEX_MD = SKILLS_DIR / "INDEX.md"
PROJECT_START_MD = GOVERNANCE_DIR / "project-start.md"
SKILLS_GOVERNANCE_MD = GOVERNANCE_DIR / "skills-governance.md"
KICKOFF_MD = GOVERNANCE_DIR / "kickoff.md"
BOOTSTRAP_CLEANUP_MD = GOVERNANCE_DIR / "bootstrap-cleanup.md"
PROJECT_STARTER_SKILL = LOCAL_DIR / "project-starter.skill"

ROOT_README_MD = REPO_ROOT / "README.md"
ROOT_COMECAR_MD = REPO_ROOT / "COMECAR-PROJETO.md"
ROOT_AGENTS_MD = REPO_ROOT / "AGENTS.md"
ROOT_STARTER_SENTINEL = REPO_ROOT / ".starter-framework-repo"

BOOTSTRAP_SCRIPT = SKILLS_DIR / "scripts" / "clean-framework-artifacts.sh"

TABLE_SKILL_RE = re.compile(r"^\|\s+[`*]{1,2}([a-z0-9-]+\.skill)[`*]{1,2}\s+\|", re.MULTILINE)
CODE_TOKEN_RE = re.compile(r"`([^`]+)`")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
VALIDATOR_MAPPING_RE = re.compile(r'"([^"]+\.yaml)"\s*:\s*"([^"]+\.schema\.json)"')

RUNTIME_VALIDATOR_REQUIRED = {
    "index.yaml",
    "context.yaml",
    "stack.yaml",
    "rules.yaml",
    "state.yaml",
    "active-feature.yaml",
    "decisions.yaml",
    "routes.yaml",
    "architecture.yaml",
    "qa.yaml",
    "handoff.yaml",
}

OUTPUT_TEMPLATE_PAIRS = [
    ("briefing-template.md", "PROJECT_BRIEF.md"),
    ("roadmap-template.md", "ROADMAP.md"),
    ("architecture-template.md", "ARCHITECTURE.md"),
]

MODEL_ORCHESTRATION_MD = GOVERNANCE_DIR / "model-orchestration.md"

DOC_SNIPPETS = {
    ROOT_README_MD: ["skills/", "AGENTS.md", "Começar projeto"],
    ROOT_COMECAR_MD: ["skills/", "AGENTS.md", "Começar projeto"],
    ROOT_AGENTS_MD: [
        "bash skills/scripts/clean-framework-artifacts.sh",
        "skills/governance/kickoff.md",
        "project-starter.skill",
        "COMECAR-PROJETO.md",
        "0g",
    ],
    KICKOFF_MD: [
        "governance/bootstrap-cleanup.md",
        "bash skills/scripts/clean-framework-artifacts.sh",
        "skills/runtime/",
        "skills/outputs/",
        "governance/project-start.md",
    ],
    PROJECT_START_MD: [
        "templates/runtime/",
        "skills/outputs/",
        "outputs/ARCHITECTURE.md",
        "python3 skills/runtime/validate.py",
    ],
    PROJECT_STARTER_SKILL: [
        "governance/bootstrap-cleanup.md",
        "governance/kickoff.md",
        "python3 skills/runtime/validate.py",
        "skills/outputs/",
    ],
    INDEX_MD: [
        "../COMECAR-PROJETO.md",
        "governance/kickoff.md",
        "scripts/clean-framework-artifacts.sh",
        "validate-skills.py",
    ],
}

SKIP_MARKDOWN_PARTS = {".git", ".venv", "__pycache__", ".cursor", "node_modules", "_lab"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def list_skill_stems(directory: Path, recursive: bool = False) -> set[str]:
    pattern = "**/*.skill" if recursive else "*.skill"
    return {p.stem for p in directory.glob(pattern) if p.is_file()}


def extract_section(text: str, start_marker: str, end_marker: str) -> str:
    start = text.find(start_marker)
    if start == -1:
        return ""
    end = text.find(end_marker, start)
    if end == -1:
        return text[start:]
    return text[start:end]


def parse_dot_list(text: str) -> list[str]:
    return [part.strip().strip("`") for part in text.split("·") if part.strip()]


def extract_start_local_resolution_ids(text: str) -> list[str]:
    lines = text.splitlines()
    items: list[str] = []
    collecting = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("2. local-skills/"):
            collecting = True
            rhs = stripped.split("→", 1)[1] if "→" in stripped else ""
            items.extend(parse_dot_list(rhs))
            continue

        if collecting:
            if re.match(r"^\d+\.", stripped):
                break
            items.extend(parse_dot_list(stripped))

    return items


def extract_readme_local_table_ids(text: str) -> set[str]:
    # Suporta tanto o header antigo (README.md) quanto o novo (INDEX.md)
    section = extract_section(text, "## Skills ativas (`local-skills/`)", "\n---")
    if not section:
        section = extract_section(text, "## 🔧 `/local-skills`", "## 🔗 `/linked-skills`")
    return {match[:-6] for match in TABLE_SKILL_RE.findall(section)}


def extract_start_routing_skill_ids(text: str) -> set[str]:
    # Suporta header com ou sem emoji
    section = extract_section(text, "## Roteamento por intenção", "**Score:**")
    if not section:
        section = extract_section(text, "## 🗺️ Roteamento por intenção", "**Score:**")
    tokens = CODE_TOKEN_RE.findall(section)
    out: set[str] = set()

    for token in tokens:
        if "/" in token or token.endswith(".md") or token.endswith(".yaml"):
            continue
        if token.startswith("cat."):
            continue
        out.add(token)

    return out


def contains_any(text: str, snippets: list[str]) -> bool:
    return any(snippet in text for snippet in snippets)


def collect_markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in REPO_ROOT.rglob("*.md"):
        if any(part in SKIP_MARKDOWN_PARTS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def extract_local_links(text: str) -> list[str]:
    links: list[str] = []
    for raw_target in MARKDOWN_LINK_RE.findall(text):
        target = raw_target.strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean = target.split("#", 1)[0].split("?", 1)[0].strip()
        if clean:
            links.append(clean)
    return links


def compare_exact(path_a: Path, path_b: Path, label: str) -> list[str]:
    if read_text(path_a) != read_text(path_b):
        return [f"{label} fora de sincronia: {rel(path_a)} != {rel(path_b)}"]
    return []


def list_relative_files(directory: Path) -> set[str]:
    return {
        str(path.relative_to(directory))
        for path in directory.rglob("*")
        if path.is_file()
    }


def extract_validator_targets(path: Path) -> set[str]:
    text = read_text(path)
    return {yaml_name for yaml_name, _ in VALIDATOR_MAPPING_RE.findall(text)}


def validate_skill_catalog() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    passes: list[str] = []

    local_stems = list_skill_stems(LOCAL_DIR)
    structure_stems = list_skill_stems(STRUCTURE_DIR)
    deferred_stems = list_skill_stems(DEFERRED_DIR, recursive=True)

    start_text = read_text(START_MD)
    readme_text = read_text(INDEX_MD)   # README.md unificado em INDEX.md (Plano 6)
    index_text = read_text(INDEX_MD)
    project_start_text = read_text(PROJECT_START_MD)
    governance_text = read_text(SKILLS_GOVERNANCE_MD)

    start_local_ids = set(extract_start_local_resolution_ids(start_text))
    if start_local_ids != local_stems:
        missing = sorted(local_stems - start_local_ids)
        extra = sorted(start_local_ids - local_stems)
        if missing:
            errors.append(
                "Start.md não lista todas as local-skills ativas: " + ", ".join(missing)
            )
        if extra:
            errors.append(
                "Start.md lista local-skills inexistentes: " + ", ".join(extra)
            )
    else:
        passes.append("OK   skill-catalog:start-local")

    start_routing_ids = extract_start_routing_skill_ids(start_text)
    unknown_routing_ids = sorted(start_routing_ids - local_stems)
    if unknown_routing_ids:
        errors.append(
            "Start.md roteia skills não ativas ou inexistentes: "
            + ", ".join(unknown_routing_ids)
        )
    else:
        passes.append("OK   skill-catalog:routing")

    deferred_leaks = sorted(deferred_stems & start_routing_ids)
    if deferred_leaks:
        errors.append(
            "Start.md expõe skills de _deferred no roteamento ativo: "
            + ", ".join(deferred_leaks)
        )
    else:
        passes.append("OK   skill-catalog:deferred")

    future_fallback_snippets = [
        "`skills.sh` → cache → executar",
        "`skills.sh` → cache/remote-skills/",
        "`linked-skills/kickoff-doc`",
        "`https://skills.sh/`",
    ]
    future_errors: list[str] = []
    if contains_any(start_text, future_fallback_snippets):
        future_errors.append("Start.md ainda trata fallback remoto como fluxo ativo.")
    if contains_any(project_start_text, future_fallback_snippets):
        future_errors.append("project-start.md ainda trata fallback remoto como fluxo ativo.")
    if future_errors:
        errors.extend(future_errors)
    else:
        passes.append("OK   skill-catalog:fallback")

    readme_local_ids = extract_readme_local_table_ids(readme_text)
    if readme_local_ids != local_stems:
        missing = sorted(local_stems - readme_local_ids)
        extra = sorted(readme_local_ids - local_stems)
        if missing:
            errors.append(
                "README.md não documenta todas as local-skills ativas: "
                + ", ".join(missing)
            )
        if extra:
            errors.append(
                "README.md documenta local-skills inexistentes: " + ", ".join(extra)
            )
    else:
        passes.append("OK   skill-catalog:readme")

    index_errors: list[str] = []
    if "- **Ativas:** `structure/` + `local-skills/`" not in index_text:
        index_errors.append("INDEX.md não marca as capabilities ativas corretamente.")
    if "- **Adiadas:** `_deferred/`" not in index_text:
        index_errors.append("INDEX.md não marca as capabilities adiadas corretamente.")
    if "- **Futuras:** `linked-skills/` + `cache/`" not in index_text:
        index_errors.append("INDEX.md não marca as capabilities futuras corretamente.")
    if index_errors:
        errors.extend(index_errors)
    else:
        passes.append("OK   skill-catalog:index")

    governance_required_snippets = [
        "`skills/local-skills/*.skill`",
        "`skills/structure/*.skill`",
        "`skills/_deferred/**`",
        "`skills/linked-skills/`",
        "`skills/cache/`",
        "fallback por `skills.sh`",
    ]
    governance_errors = [
        f"skills-governance.md não contém a definição obrigatória: {snippet}"
        for snippet in governance_required_snippets
        if snippet not in governance_text
    ]
    if governance_errors:
        errors.extend(governance_errors)
    else:
        passes.append("OK   skill-catalog:governance")

    if not structure_stems:
        errors.append("Nenhuma structure skill encontrada em skills/structure/.")
    else:
        passes.append("OK   skill-catalog:structure")

    linked_has_files = LINKED_DIR.exists() and any(p.is_file() for p in LINKED_DIR.rglob("*"))
    cache_has_files = CACHE_DIR.exists() and any(p.is_file() for p in CACHE_DIR.rglob("*"))

    capability_errors: list[str] = []
    if linked_has_files and "capability futura" in readme_text.lower():
        capability_errors.append(
            "linked-skills/ já tem arquivos, mas README.md ainda o marca apenas como capability futura."
        )
    if cache_has_files and "cache remoto futuro" in readme_text.lower():
        capability_errors.append(
            "skills/cache/ já tem conteúdo, mas README.md ainda o marca apenas como reservado."
        )
    if capability_errors:
        errors.extend(capability_errors)
    else:
        passes.append("OK   skill-catalog:capabilities")

    return passes, errors


def validate_markdown_links() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    for md_path in collect_markdown_files():
        text = read_text(md_path)
        for target in extract_local_links(text):
            if target.startswith("/"):
                continue
            resolved = (md_path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"Link quebrado em {rel(md_path)} -> {target}")

    if errors:
        return [], errors
    return ["OK   docs:links"], []


def validate_doc_snippets() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    for path, snippets in DOC_SNIPPETS.items():
        text = read_text(path)
        for snippet in snippets:
            if snippet not in text:
                errors.append(f"Doc obrigatório sem referência esperada em {rel(path)}: {snippet}")

    if errors:
        return [], errors
    return ["OK   docs:references"], []


def validate_template_output_consistency() -> tuple[list[str], list[str]]:
    errors: list[str] = []

    for template_name, output_name in OUTPUT_TEMPLATE_PAIRS:
        template_path = TEMPLATES_DIR / template_name
        output_path = OUTPUTS_DIR / output_name
        if not template_path.exists():
            errors.append(f"Template obrigatório ausente: {rel(template_path)}")
            continue
        if not output_path.exists():
            errors.append(f"Output obrigatório ausente: {rel(output_path)}")
            continue
        errors.extend(compare_exact(template_path, output_path, "Template/output"))

    if errors:
        return [], errors
    return ["OK   templates:outputs"], []


def validate_runtime_template_mirror() -> tuple[list[str], list[str]]:
    errors: list[str] = []

    mirror_pairs = [
        (RUNTIME_DIR / "validate.py", TEMPLATE_RUNTIME_DIR / "validate.py"),
        (RUNTIME_DIR / "requirements-runtime.txt", TEMPLATE_RUNTIME_DIR / "requirements-runtime.txt"),
    ]
    for current_path, template_path in mirror_pairs:
        if not current_path.exists():
            errors.append(f"Arquivo runtime ausente: {rel(current_path)}")
            continue
        if not template_path.exists():
            errors.append(f"Arquivo template runtime ausente: {rel(template_path)}")
            continue
        errors.extend(compare_exact(current_path, template_path, "Runtime/template"))

    runtime_schema_dir = RUNTIME_DIR / "schema"
    template_schema_dir = TEMPLATE_RUNTIME_DIR / "schema"
    if not runtime_schema_dir.exists():
        errors.append(f"Diretório ausente: {rel(runtime_schema_dir)}")
    if not template_schema_dir.exists():
        errors.append(f"Diretório ausente: {rel(template_schema_dir)}")

    if runtime_schema_dir.exists() and template_schema_dir.exists():
        runtime_files = list_relative_files(runtime_schema_dir)
        template_files = list_relative_files(template_schema_dir)
        missing_in_runtime = sorted(template_files - runtime_files)
        missing_in_template = sorted(runtime_files - template_files)
        if missing_in_runtime:
            errors.append(
                "Schema runtime sem espelho em templates/runtime/schema/: "
                + ", ".join(missing_in_runtime)
            )
        if missing_in_template:
            errors.append(
                "Schema template sem espelho em runtime/schema/: "
                + ", ".join(missing_in_template)
            )
        for relative_path in sorted(runtime_files & template_files):
            errors.extend(
                compare_exact(
                    runtime_schema_dir / relative_path,
                    template_schema_dir / relative_path,
                    "Schema/runtime",
                )
            )

    for validator_path in [RUNTIME_DIR / "validate.py", TEMPLATE_RUNTIME_DIR / "validate.py"]:
        if not validator_path.exists():
            continue
        targets = extract_validator_targets(validator_path)
        missing = sorted(RUNTIME_VALIDATOR_REQUIRED - targets)
        if missing:
            errors.append(
                f"Validador incompleto em {rel(validator_path)}: faltam "
                + ", ".join(missing)
            )

    if errors:
        return [], errors
    return ["OK   runtime:mirror"], []


def validate_repo_hygiene() -> tuple[list[str], list[str]]:
    """Delega para check-repo-hygiene.py — arquivos que não devem estar versionados."""
    checker = SKILLS_DIR / "scripts" / "check-repo-hygiene.py"
    if not checker.exists():
        return [], [f"Script ausente: {rel(checker)}"]

    import subprocess

    result = subprocess.run(
        [sys.executable, str(checker)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stdout or result.stderr or "").strip()
        return [], [f"Repo hygiene: violações detectadas\n{detail}"]
    return ["OK   repo:hygiene"], []


def validate_model_orchestration_log() -> tuple[list[str], list[str]]:
    """Garante protocolo §0g com log TDD e racionalizações documentadas."""
    errors: list[str] = []
    path = MODEL_ORCHESTRATION_MD
    if not path.exists():
        return [], [f"Protocolo ausente: {rel(path)}"]

    text = read_text(path)
    required_sections = [
        "## Log de testes (TDD)",
        "## Racionalizações proibidas",
    ]
    for section in required_sections:
        if section not in text:
            errors.append(f"{rel(path)} sem seção obrigatória: {section}")

    log_markers = ["**RED:**", "**GREEN:**", "**REFACTOR"]
    for marker in log_markers:
        if marker not in text:
            errors.append(f"{rel(path)} log TDD incompleto: falta linha com {marker}")

    if errors:
        return [], errors
    return ["OK   governance:model-orchestration-log"], []


def validate_bootstrap_contract() -> tuple[list[str], list[str]]:
    errors: list[str] = []

    required_paths = [
        ROOT_STARTER_SENTINEL,
        BOOTSTRAP_SCRIPT,
        ROOT_README_MD,
        ROOT_COMECAR_MD,
        ROOT_AGENTS_MD,
        KICKOFF_MD,
        BOOTSTRAP_CLEANUP_MD,
        PROJECT_START_MD,
        PROJECT_STARTER_SKILL,
    ]
    for path in required_paths:
        if not path.exists():
            errors.append(f"Artefato obrigatório de bootstrap ausente: {rel(path)}")

    if BOOTSTRAP_SCRIPT.exists():
        script_text = read_text(BOOTSTRAP_SCRIPT)
        script_required_snippets = [
            "#!/usr/bin/env bash",
            "set -euo pipefail",
            ".starter-framework-repo",
            'rm -rf skills/runtime',
            'rm -rf skills/outputs',
            'echo "Mantido: skills/ (governance, templates, local-skills, …), AGENTS.md"',
        ]
        for snippet in script_required_snippets:
            if snippet not in script_text:
                errors.append(
                    f"Bootstrap script sem proteção/contrato esperado: {snippet}"
                )

    if errors:
        return [], errors
    return ["OK   bootstrap"], []


# Orçamento de contexto (bytes) — economia verificável, não declarada.
# Grupos refletem o custo real de carga por sessão (AGENTS.md §2: hot/warm).
# Limites = estado atual + folga pequena; aumentar limite exige decisão registrada.
CONTEXT_BUDGETS: dict[str, tuple[list[Path], int]] = {
    "hot (toda sessão)": (
        [
            ROOT_AGENTS_MD,
            RUNTIME_DIR / "index.yaml",
            RUNTIME_DIR / "rules.yaml",
            RUNTIME_DIR / "context.yaml",
            RUNTIME_DIR / "state.yaml",
            GOVERNANCE_DIR / "Start-ops.md",
        ],
        20_000,
    ),
    "warm (sob demanda frequente)": (
        [
            RUNTIME_DIR / "handoff.yaml",
            RUNTIME_DIR / "qa.yaml",
            RUNTIME_DIR / "active-feature.yaml",
        ],
        8_000,
    ),
    "entrada (docs de orientação)": (
        [INDEX_MD, ROOT_COMECAR_MD],   # README.md + STRUCTURE.md unificados em INDEX.md (Plano 6)
        24_000,
    ),
}

GOVERNANCE_TOTAL_BUDGET = 130_000
GOVERNANCE_FILE_BUDGET = 14_000
LOCAL_SKILL_FILE_BUDGET = 20_000


def validate_context_budget() -> tuple[list[str], list[str]]:
    """Falha se o peso de contexto regredir além do orçamento por camada."""
    passes: list[str] = []
    errors: list[str] = []

    for group, (files, limit) in CONTEXT_BUDGETS.items():
        total = 0
        for f in files:
            if not f.exists():
                errors.append(f"budget: arquivo ausente no grupo '{group}': {rel(f)}")
                continue
            total += f.stat().st_size
        if total > limit:
            errors.append(
                f"budget: grupo '{group}' estourou — {total:,} bytes > limite {limit:,}"
            )
        else:
            passes.append(f"OK   budget:{group} ({total:,}/{limit:,} bytes)")

    gov_files = sorted(GOVERNANCE_DIR.glob("*.md"))
    gov_total = sum(f.stat().st_size for f in gov_files)
    if gov_total > GOVERNANCE_TOTAL_BUDGET:
        errors.append(
            f"budget: governance/ total {gov_total:,} bytes > limite {GOVERNANCE_TOTAL_BUDGET:,}"
        )
    else:
        passes.append(
            f"OK   budget:governance-total ({gov_total:,}/{GOVERNANCE_TOTAL_BUDGET:,} bytes)"
        )
    for f in gov_files:
        if f.stat().st_size > GOVERNANCE_FILE_BUDGET:
            errors.append(
                f"budget: {rel(f)} tem {f.stat().st_size:,} bytes > limite por arquivo {GOVERNANCE_FILE_BUDGET:,}"
            )

    oversized_skills = [
        f
        for f in sorted(LOCAL_DIR.glob("*.skill"))
        if f.stat().st_size > LOCAL_SKILL_FILE_BUDGET
    ]
    for f in oversized_skills:
        errors.append(
            f"budget: {rel(f)} tem {f.stat().st_size:,} bytes > limite por skill {LOCAL_SKILL_FILE_BUDGET:,}"
        )
    if not oversized_skills:
        passes.append(
            f"OK   budget:local-skills (todas ≤ {LOCAL_SKILL_FILE_BUDGET:,} bytes)"
        )

    return passes, errors


def validate() -> tuple[list[str], list[str]]:
    passes: list[str] = []
    errors: list[str] = []

    for validator in [
        validate_skill_catalog,
        validate_markdown_links,
        validate_doc_snippets,
        validate_model_orchestration_log,
        validate_template_output_consistency,
        validate_runtime_template_mirror,
        validate_repo_hygiene,
        validate_bootstrap_contract,
        validate_context_budget,
    ]:
        ok_items, err_items = validator()
        passes.extend(ok_items)
        errors.extend(err_items)

    return passes, errors


def main() -> int:
    passes, errors = validate()
    if errors:
        print("FAIL system")
        for error in errors:
            print(f"  - {error}")
        print(f"\n{len(passes)} passed, {len(errors)} failed")
        return 1

    for item in passes:
        print(item)
    print(f"\n{len(passes)} passed, 0 failed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
