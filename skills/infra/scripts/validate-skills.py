#!/usr/bin/env python3
"""
STARTER System Validator.

Valida antidrift entre filesystem, docs centrais, templates, outputs e bootstrap.

Uso:
  python3 skills/infra/scripts/validate-skills.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILLS_DIR = REPO_ROOT / "skills"
FLOWS_DIR = SKILLS_DIR / "flows"

LOCAL_DIR = SKILLS_DIR / "catalog"
STRUCTURE_DIR = SKILLS_DIR / "structure"
DEFERRED_DIR = SKILLS_DIR / "_deferred"
LINKED_DIR = SKILLS_DIR / "linked-skills"
CACHE_DIR = SKILLS_DIR / "cache"
TEMPLATES_DIR = SKILLS_DIR / "templates"
OUTPUTS_DIR = SKILLS_DIR / "outputs"
RUNTIME_DIR = SKILLS_DIR / "core" / "runtime"
TEMPLATE_RUNTIME_DIR = TEMPLATES_DIR / "runtime"

START_MD = FLOWS_DIR / "Start.md"
README_MD = SKILLS_DIR / "README.md"
INDEX_MD = SKILLS_DIR / "INDEX.md"
PROJECT_START_MD = FLOWS_DIR / "project-start.md"
SKILLS_GOVERNANCE_MD = FLOWS_DIR / "skills-governance.md"
KICKOFF_MD = FLOWS_DIR / "kickoff.md"
BOOTSTRAP_CLEANUP_MD = FLOWS_DIR / "bootstrap-cleanup.md"
PROJECT_STARTER_SKILL = LOCAL_DIR / "project-starter.skill"

ROOT_README_MD = REPO_ROOT / "README.md"
ROOT_COMECAR_MD = REPO_ROOT / "COMECAR-PROJETO.md"
ROOT_AGENTS_MD = REPO_ROOT / "AGENTS.md"
ROOT_STARTER_SENTINEL = REPO_ROOT / ".starter-framework-repo"

BOOTSTRAP_SCRIPT = SKILLS_DIR / "infra" / "scripts" / "clean-framework-artifacts.sh"

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

MODEL_ORCHESTRATION_MD = FLOWS_DIR / "model-orchestration.md"

DOC_SNIPPETS = {
    ROOT_README_MD: ["skills/", "AGENTS.md", "Começar projeto"],
    ROOT_COMECAR_MD: ["skills/", "AGENTS.md", "Começar projeto"],
    ROOT_AGENTS_MD: [
        "bash skills/infra/scripts/clean-framework-artifacts.sh",
        "skills/flows/kickoff.md",
        "project-starter.skill",
        "COMECAR-PROJETO.md",
        "0g",
    ],
    KICKOFF_MD: [
        "flows/bootstrap-cleanup.md",
        "bash skills/infra/scripts/clean-framework-artifacts.sh",
        "skills/core/runtime/",
        "skills/outputs/",
        "flows/project-start.md",
    ],
    PROJECT_START_MD: [
        "templates/runtime/",
        "skills/outputs/",
        "outputs/ARCHITECTURE.md",
        "python3 skills/core/runtime/validate.py",
    ],
    PROJECT_STARTER_SKILL: [
        "flows/bootstrap-cleanup.md",
        "flows/kickoff.md",
        "python3 skills/core/runtime/validate.py",
        "skills/outputs/",
    ],
    INDEX_MD: [
        "../COMECAR-PROJETO.md",
        "flows/kickoff.md",
        "scripts/clean-framework-artifacts.sh",
        "validate-skills.py",
    ],
}

SKIP_MARKDOWN_PARTS = {".git", ".venv", "__pycache__", ".cursor", "node_modules", "_lab", "_archive"}


def read_text(path: Path) -> str:
    """Lê arquivo de texto com encoding UTF-8."""
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    """Retorna o caminho relativo ao REPO_ROOT como string (fallback para path absoluto)."""
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def list_skill_stems(directory: Path, recursive: bool = False) -> set[str]:
    """Retorna o conjunto de stems (nomes sem extensão) dos arquivos .skill no diretório."""
    pattern = "**/*.skill" if recursive else "*.skill"
    return {p.stem for p in directory.glob(pattern) if p.is_file()}


def extract_section(text: str, start_marker: str, end_marker: str) -> str:
    """Extrai a substring entre start_marker e end_marker; retorna '' se start não encontrado."""
    start = text.find(start_marker)
    if start == -1:
        return ""
    end = text.find(end_marker, start)
    if end == -1:
        return text[start:]
    return text[start:end]


def parse_dot_list(text: str) -> list[str]:
    """Divide texto separado por '·' e retorna itens sem backticks e espaços."""
    return [part.strip().strip("`") for part in text.split("·") if part.strip()]


def extract_start_local_resolution_ids(text: str) -> list[str]:
    """Extrai IDs de skills listados na seção '2. catalog/' do Start.md."""
    lines = text.splitlines()
    items: list[str] = []
    collecting = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("2. catalog/"):
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
    """Extrai stems de skills da tabela de local-skills no README/INDEX.md."""
    # Suporta tanto o header antigo (README.md) quanto o novo (INDEX.md)
    section = extract_section(text, "## Skills ativas (`catalog/`)", "\n---")
    if not section:
        section = extract_section(text, "## 🔧 `/local-skills`", "## 🔗 `/linked-skills`")
    return {match[:-6] for match in TABLE_SKILL_RE.findall(section)}


def extract_start_routing_skill_ids(text: str) -> set[str]:
    """Extrai IDs de skills referenciados no roteamento por intenção do Start.md."""
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
    """Retorna True se qualquer snippet estiver presente no texto."""
    return any(snippet in text for snippet in snippets)


def collect_markdown_files() -> list[Path]:
    """Coleta todos os arquivos .md do repositório, excluindo pastas irrelevantes."""
    files: list[Path] = []
    for path in REPO_ROOT.rglob("*.md"):
        if any(part in SKIP_MARKDOWN_PARTS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def extract_local_links(text: str) -> list[str]:
    """Extrai hrefs de links locais (não-http, não-âncora) de um texto markdown."""
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
    """Retorna lista de erros se os dois arquivos não forem byte-a-byte idênticos."""
    if read_text(path_a) != read_text(path_b):
        return [f"{label} fora de sincronia: {rel(path_a)} != {rel(path_b)}"]
    return []


def list_relative_files(directory: Path) -> set[str]:
    """Lista todos os arquivos do diretório como caminhos relativos ao próprio diretório."""
    return {
        str(path.relative_to(directory))
        for path in directory.rglob("*")
        if path.is_file()
    }


def extract_validator_targets(path: Path) -> set[str]:
    """Extrai os nomes de arquivos YAML mapeados pelo validador runtime."""
    text = read_text(path)
    return {yaml_name for yaml_name, _ in VALIDATOR_MAPPING_RE.findall(text)}


def _check_start_local_resolution(
    local_stems: set[str], start_text: str
) -> tuple[list[str], list[str]]:
    """Verifica que Start.md lista exatamente as skills ativas em catalog/."""
    start_local_ids = set(extract_start_local_resolution_ids(start_text))
    if start_local_ids == local_stems:
        return ["OK   skill-catalog:start-local"], []
    errors: list[str] = []
    missing = sorted(local_stems - start_local_ids)
    extra = sorted(start_local_ids - local_stems)
    if missing:
        errors.append("Start.md não lista todas as local-skills ativas: " + ", ".join(missing))
    if extra:
        errors.append("Start.md lista local-skills inexistentes: " + ", ".join(extra))
    return [], errors


def _check_start_routing(
    local_stems: set[str], deferred_stems: set[str], start_text: str
) -> tuple[list[str], list[str]]:
    """Verifica que o roteamento do Start.md não aponta para skills inexistentes ou adiadas."""
    passes: list[str] = []
    errors: list[str] = []
    start_routing_ids = extract_start_routing_skill_ids(start_text)

    unknown = sorted(start_routing_ids - local_stems)
    if unknown:
        errors.append("Start.md roteia skills não ativas ou inexistentes: " + ", ".join(unknown))
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

    return passes, errors


def _check_fallback_snippets(start_text: str, project_start_text: str) -> tuple[list[str], list[str]]:
    """Verifica que nenhum doc trata fallback remoto como fluxo ativo."""
    future_fallback_snippets = [
        "`skills.sh` → cache → executar",
        "`skills.sh` → cache/remote-skills/",
        "`linked-skills/kickoff-doc`",
        "`https://skills.sh/`",
    ]
    errors: list[str] = []
    if contains_any(start_text, future_fallback_snippets):
        errors.append("Start.md ainda trata fallback remoto como fluxo ativo.")
    if contains_any(project_start_text, future_fallback_snippets):
        errors.append("project-start.md ainda trata fallback remoto como fluxo ativo.")
    if errors:
        return [], errors
    return ["OK   skill-catalog:fallback"], []


def _check_readme_local_table(
    local_stems: set[str], readme_text: str
) -> tuple[list[str], list[str]]:
    """Verifica que a tabela de local-skills no README/INDEX.md está sincronizada com o filesystem."""
    readme_local_ids = extract_readme_local_table_ids(readme_text)
    if readme_local_ids == local_stems:
        return ["OK   skill-catalog:readme"], []
    errors: list[str] = []
    missing = sorted(local_stems - readme_local_ids)
    extra = sorted(readme_local_ids - local_stems)
    if missing:
        errors.append("README.md não documenta todas as local-skills ativas: " + ", ".join(missing))
    if extra:
        errors.append("README.md documenta local-skills inexistentes: " + ", ".join(extra))
    return [], errors


def _check_index_markers(index_text: str) -> tuple[list[str], list[str]]:
    """Verifica que o INDEX.md marca corretamente capabilities ativas, adiadas e futuras."""
    required = {
        "- **Ativas:** `structure/` + `catalog/`": "INDEX.md não marca as capabilities ativas corretamente.",
        "- **Adiadas:** `_deferred/`": "INDEX.md não marca as capabilities adiadas corretamente.",
        "- **Futuras:** `linked-skills/` + `cache/`": "INDEX.md não marca as capabilities futuras corretamente.",
    }
    errors = [msg for marker, msg in required.items() if marker not in index_text]
    if errors:
        return [], errors
    return ["OK   skill-catalog:index"], []


def _check_governance_snippets(governance_text: str) -> tuple[list[str], list[str]]:
    """Verifica que skills-governance.md contém todas as definições obrigatórias."""
    required_snippets = [
        "`skills/catalog/*.skill`",
        "`skills/structure/*.skill`",
        "`skills/_deferred/**`",
        "`skills/linked-skills/`",
        "`skills/cache/`",
        "fallback por `skills.sh`",
    ]
    errors = [
        f"skills-governance.md não contém a definição obrigatória: {s}"
        for s in required_snippets
        if s not in governance_text
    ]
    if errors:
        return [], errors
    return ["OK   skill-catalog:governance"], []


def _check_structure_and_capabilities(
    structure_stems: set[str], readme_text: str
) -> tuple[list[str], list[str]]:
    """Verifica que structure skills existem e que capabilities futuras não são promovidas indevidamente."""
    passes: list[str] = []
    errors: list[str] = []

    if not structure_stems:
        errors.append("Nenhuma structure skill encontrada em skills/structure/.")
    else:
        passes.append("OK   skill-catalog:structure")

    linked_has_files = LINKED_DIR.exists() and any(p.is_file() for p in LINKED_DIR.rglob("*"))
    cache_has_files = CACHE_DIR.exists() and any(p.is_file() for p in CACHE_DIR.rglob("*"))

    if linked_has_files and "capability futura" in readme_text.lower():
        errors.append(
            "linked-skills/ já tem arquivos, mas README.md ainda o marca apenas como capability futura."
        )
    if cache_has_files and "cache remoto futuro" in readme_text.lower():
        errors.append(
            "skills/cache/ já tem conteúdo, mas README.md ainda o marca apenas como reservado."
        )
    if not errors or (not linked_has_files and not cache_has_files):
        if linked_has_files or cache_has_files:
            pass  # erros já adicionados acima
        else:
            passes.append("OK   skill-catalog:capabilities")

    return passes, errors


def validate_skill_catalog() -> tuple[list[str], list[str]]:
    """Verifica coerência entre arquivos .skill no filesystem e suas referências nos docs."""
    passes: list[str] = []
    errors: list[str] = []

    local_stems = list_skill_stems(LOCAL_DIR)
    structure_stems = list_skill_stems(STRUCTURE_DIR)
    deferred_stems = list_skill_stems(DEFERRED_DIR, recursive=True)

    start_text = read_text(START_MD)
    index_text = read_text(INDEX_MD)
    project_start_text = read_text(PROJECT_START_MD)
    governance_text = read_text(SKILLS_GOVERNANCE_MD)

    for checker_passes, checker_errors in [
        _check_start_local_resolution(local_stems, start_text),
        _check_start_routing(local_stems, deferred_stems, start_text),
        _check_fallback_snippets(start_text, project_start_text),
        _check_readme_local_table(local_stems, index_text),
        _check_index_markers(index_text),
        _check_governance_snippets(governance_text),
        _check_structure_and_capabilities(structure_stems, index_text),
    ]:
        passes.extend(checker_passes)
        errors.extend(checker_errors)

    return passes, errors


def validate_markdown_links() -> tuple[list[str], list[str]]:
    """Verifica se todos os links locais em arquivos .md resolvem para arquivos existentes."""
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
    """Verifica que cada doc obrigatório contém os trechos de referência esperados."""
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
    """Verifica que cada template de output tem cópia idêntica em skills/outputs/."""
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


def _check_runtime_file_mirrors(errors: list[str]) -> None:
    """Verifica que validate.py e requirements-runtime.txt têm cópias idênticas no template."""
    mirror_pairs = [
        (RUNTIME_DIR / "validate.py", TEMPLATE_RUNTIME_DIR / "validate.py"),
        (RUNTIME_DIR / "requirements-runtime.txt", TEMPLATE_RUNTIME_DIR / "requirements-runtime.txt"),
    ]
    for current_path, template_path in mirror_pairs:
        if not current_path.exists():
            errors.append(f"Arquivo runtime ausente: {rel(current_path)}")
        elif not template_path.exists():
            errors.append(f"Arquivo template runtime ausente: {rel(template_path)}")
        else:
            errors.extend(compare_exact(current_path, template_path, "Runtime/template"))


def _check_schema_mirror(errors: list[str]) -> None:
    """Verifica que todos os schemas JSON estão espelhados entre runtime/schema/ e templates/runtime/schema/."""
    runtime_schema_dir = RUNTIME_DIR / "schema"
    template_schema_dir = TEMPLATE_RUNTIME_DIR / "schema"

    if not runtime_schema_dir.exists():
        errors.append(f"Diretório ausente: {rel(runtime_schema_dir)}")
    if not template_schema_dir.exists():
        errors.append(f"Diretório ausente: {rel(template_schema_dir)}")
        return

    if not runtime_schema_dir.exists():
        return

    runtime_files = list_relative_files(runtime_schema_dir)
    template_files = list_relative_files(template_schema_dir)

    missing_in_runtime = sorted(template_files - runtime_files)
    missing_in_template = sorted(runtime_files - template_files)
    if missing_in_runtime:
        errors.append("Schema runtime sem espelho em templates/runtime/schema/: " + ", ".join(missing_in_runtime))
    if missing_in_template:
        errors.append("Schema template sem espelho em runtime/schema/: " + ", ".join(missing_in_template))

    for relative_path in sorted(runtime_files & template_files):
        errors.extend(compare_exact(runtime_schema_dir / relative_path, template_schema_dir / relative_path, "Schema/runtime"))


def _check_validator_completeness(errors: list[str]) -> None:
    """Verifica que cada validate.py cobre todos os YAMLs obrigatórios."""
    for validator_path in [RUNTIME_DIR / "validate.py", TEMPLATE_RUNTIME_DIR / "validate.py"]:
        if not validator_path.exists():
            continue
        missing = sorted(RUNTIME_VALIDATOR_REQUIRED - extract_validator_targets(validator_path))
        if missing:
            errors.append(f"Validador incompleto em {rel(validator_path)}: faltam " + ", ".join(missing))


def validate_runtime_template_mirror() -> tuple[list[str], list[str]]:
    """Verifica que os arquivos runtime estão espelhados identicamente em templates/runtime/."""
    errors: list[str] = []
    _check_runtime_file_mirrors(errors)
    _check_schema_mirror(errors)
    _check_validator_completeness(errors)
    if errors:
        return [], errors
    return ["OK   runtime:mirror"], []


def validate_repo_hygiene() -> tuple[list[str], list[str]]:
    """Delega para check-repo-hygiene.py — arquivos que não devem estar versionados."""
    checker = SKILLS_DIR / "infra" / "scripts" / "check-repo-hygiene.py"
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
    """Verifica que todos os artefatos obrigatórios do bootstrap existem e são íntegros."""
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
            'rm -rf skills/core/runtime',
            'rm -rf skills/outputs',
            'echo "Mantido: skills/ (flows, templates, catalog, …), AGENTS.md"',
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
            FLOWS_DIR / "Start-ops.md",
        ],
        23_000,
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


def _check_layer_budgets(passes: list[str], errors: list[str]) -> None:
    """Verifica orçamento de bytes por camada de contexto (hot/warm/entrada)."""
    for group, (files, limit) in CONTEXT_BUDGETS.items():
        total = 0
        for f in files:
            if not f.exists():
                errors.append(f"budget: arquivo ausente no grupo '{group}': {rel(f)}")
                continue
            total += f.stat().st_size
        if total > limit:
            errors.append(f"budget: grupo '{group}' estourou — {total:,} bytes > limite {limit:,}")
        else:
            passes.append(f"OK   budget:{group} ({total:,}/{limit:,} bytes)")


def _check_governance_budget(passes: list[str], errors: list[str]) -> None:
    """Verifica que a pasta flows/ não ultrapassa os limites total e por arquivo."""
    gov_files = sorted(FLOWS_DIR.glob("*.md"))
    gov_total = sum(f.stat().st_size for f in gov_files)
    if gov_total > GOVERNANCE_TOTAL_BUDGET:
        errors.append(f"budget: flows/ total {gov_total:,} bytes > limite {GOVERNANCE_TOTAL_BUDGET:,}")
    else:
        passes.append(f"OK   budget:governance-total ({gov_total:,}/{GOVERNANCE_TOTAL_BUDGET:,} bytes)")
    for f in gov_files:
        if f.stat().st_size > GOVERNANCE_FILE_BUDGET:
            errors.append(f"budget: {rel(f)} tem {f.stat().st_size:,} bytes > limite por arquivo {GOVERNANCE_FILE_BUDGET:,}")


def _check_local_skill_budgets(passes: list[str], errors: list[str]) -> None:
    """Verifica que nenhuma local-skill ultrapassa o limite de bytes por arquivo."""
    oversized = [f for f in sorted(LOCAL_DIR.glob("*.skill")) if f.stat().st_size > LOCAL_SKILL_FILE_BUDGET]
    for f in oversized:
        errors.append(f"budget: {rel(f)} tem {f.stat().st_size:,} bytes > limite por skill {LOCAL_SKILL_FILE_BUDGET:,}")
    if not oversized:
        passes.append(f"OK   budget:local-skills (todas ≤ {LOCAL_SKILL_FILE_BUDGET:,} bytes)")


def validate_context_budget() -> tuple[list[str], list[str]]:
    """Falha se o peso de contexto regredir além do orçamento por camada."""
    passes: list[str] = []
    errors: list[str] = []
    _check_layer_budgets(passes, errors)
    _check_governance_budget(passes, errors)
    _check_local_skill_budgets(passes, errors)
    return passes, errors


# ---------------------------------------------------------------------------
# Mapa declarativo de sincronização docs ↔ runtime
# Cada entrada: (yaml_file, yaml_key_path, doc_files, expected_text, description)
#   yaml_key_path: lista de chaves para navegar no YAML
#   expected_text: texto que DEVE aparecer nos docs quando o status for o mapeado
#   A validação falha se yaml status = mapeado e nenhum doc contém expected_text
#   ou se yaml status ≠ mapeado e algum doc contém o texto proibido (negação)
# ---------------------------------------------------------------------------
_DOC_RUNTIME_SYNC_PAIRS: list[dict] = [
    {
        "id": "playwright_active",
        "yaml_file": RUNTIME_DIR / "qa.yaml",
        "yaml_path": ["phase_4_playwright", "status"],
        "expected_yaml_value": "active",
        "doc_files": [
            REPO_ROOT / "README.md",
            REPO_ROOT / "docs" / "public" / "lp-github.md",
        ],
        # texto que DEVE aparecer nos docs quando status=active
        "required_text": "Fase 4",
        # texto que NÃO pode aparecer nos docs quando status=active
        "forbidden_pattern": r"desativado.*playwright|playwright.*desativado",
        "description": "Playwright Fase 4 ativo em qa.yaml ↔ docs públicos coerentes",
    },
]


def _yaml_get(data: dict, path: list[str]):
    """Navega num dict aninhado por lista de chaves; retorna None se não encontrar."""
    for key in path:
        if not isinstance(data, dict):
            return None
        data = data.get(key)
    return data


def _check_sync_pair(pair: dict, yaml_module) -> tuple[list[str], list[str]]:
    """Avalia um único par da lista _DOC_RUNTIME_SYNC_PAIRS; retorna (passes, errors)."""
    passes: list[str] = []
    errors: list[str] = []
    pair_id: str = pair["id"]
    yaml_file: Path = pair["yaml_file"]

    if not yaml_file.exists():
        errors.append(f"doc-runtime-sync[{pair_id}]: YAML não encontrado: {rel(yaml_file)}")
        return passes, errors

    with yaml_file.open(encoding="utf-8") as fh:
        data = yaml_module.safe_load(fh)

    actual_value = _yaml_get(data, pair["yaml_path"])
    expected_value = pair["expected_yaml_value"]

    if actual_value != expected_value:
        passes.append(f"OK   doc-runtime-sync[{pair_id}]: yaml={actual_value!r} (esperado {expected_value!r} — sem restrição nos docs)")
        return passes, errors

    # YAML no estado esperado — verificar cada doc
    for doc_file in pair.get("doc_files", []):
        doc_path = Path(doc_file)
        if not doc_path.exists():
            errors.append(f"doc-runtime-sync[{pair_id}]: doc ausente: {rel(doc_path)}")
            continue
        content = doc_path.read_text(encoding="utf-8")
        yaml_key = ".".join(pair["yaml_path"])

        required = pair.get("required_text")
        if required and required not in content:
            errors.append(f"doc-runtime-sync[{pair_id}]: '{required}' ausente em {rel(doc_path)} (yaml {yaml_key}={expected_value!r})")
        else:
            passes.append(f"OK   doc-runtime-sync[{pair_id}]: texto obrigatório presente em {rel(doc_path)}")

        forbidden = pair.get("forbidden_pattern")
        if forbidden and re.search(forbidden, content, re.IGNORECASE):
            errors.append(f"doc-runtime-sync[{pair_id}]: padrão proibido '{forbidden}' encontrado em {rel(doc_path)}")

    return passes, errors


def validate_doc_runtime_sync() -> tuple[list[str], list[str]]:
    """Verifica coerência entre valores de runtime YAML e menções nos docs públicos."""
    passes: list[str] = []
    errors: list[str] = []

    try:
        import yaml  # type: ignore
    except ImportError:
        errors.append("doc-runtime-sync: módulo PyYAML não encontrado; instale com pip install pyyaml")
        return passes, errors

    if not _DOC_RUNTIME_SYNC_PAIRS:
        return ["OK   doc-runtime-sync: nenhum par configurado"], []

    for pair in _DOC_RUNTIME_SYNC_PAIRS:
        p, e = _check_sync_pair(pair, yaml)
        passes.extend(p)
        errors.extend(e)

    return passes, errors


def validate_spec_coherence() -> tuple[list[str], list[str]]:
    """Valida coerência dos spec dirs (critérios ↔ tasks, plan→tasks, Verificação)."""
    import importlib.util as _ilu

    _csc_path = Path(__file__).resolve().parent / "check-spec-coherence.py"
    if not _csc_path.is_file():
        return [], [f"check-spec-coherence.py não encontrado em {_csc_path}"]

    _spec = _ilu.spec_from_file_location("_csc", _csc_path)
    _mod = _ilu.module_from_spec(_spec)  # type: ignore[arg-type]
    _spec.loader.exec_module(_mod)  # type: ignore[union-attr]

    passes, errors = _mod.check_spec_coherence()
    labeled_passes = [f"spec-coherence: {p}" for p in passes]
    labeled_errors = [f"spec-coherence: {e}" for e in errors]
    return labeled_passes, labeled_errors


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
        validate_doc_runtime_sync,
        validate_spec_coherence,
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
