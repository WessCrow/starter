#!/usr/bin/env python3
"""
STARTER Runtime Validator — valida YAML contra JSON Schema.
Uso: python3 skills/runtime/validate.py [--file rules.yaml]
Deps: pip install pyyaml jsonschema  (ou: .venv/bin/pip install -r requirements-runtime.txt)
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

RUNTIME_DIR = Path(__file__).resolve().parent
SCHEMA_DIR = RUNTIME_DIR / "schema"

META_PROPS = {
    "v": {"type": "string", "pattern": r"^[0-9]+\.[0-9]+(\.[0-9]+)?$"},
    "updated": {"type": "string", "format": "date"},
}
META_REQUIRED = ["v", "updated"]

FILE_TO_SCHEMA = {
    "index.yaml": "index.schema.json",
    "context.yaml": "context.schema.json",
    "stack.yaml": "stack.schema.json",
    "rules.yaml": "rules.schema.json",
    "state.yaml": "state.schema.json",
    "handoff.yaml": "handoff.schema.json",
    "qa.yaml": "qa.schema.json",
    "active-feature.yaml": "active-feature.schema.json",
    "decisions.yaml": "decisions.schema.json",
    "routes.yaml": "routes.schema.json",
    "architecture.yaml": "architecture.schema.json",
}


def _import_deps():
    try:
        import yaml
        from jsonschema import Draft202012Validator
    except ImportError:
        print("Dependências ausentes: pip install pyyaml jsonschema")
        sys.exit(2)
    return yaml, Draft202012Validator


def merge_meta(schema: dict) -> dict:
    """Injeta v/updated e remove allOf/$ref para _meta."""
    s = copy.deepcopy(schema)
    s.pop("allOf", None)
    s.pop("$id", None)

    if "oneOf" in s:
        branches = [merge_meta_branch(b) for b in s["oneOf"]]
        out = {k: v for k, v in s.items() if k != "oneOf"}
        out["oneOf"] = branches
        return inject_meta(out)

    return inject_meta(s)


def merge_meta_branch(branch: dict) -> dict:
    b = copy.deepcopy(branch)
    return inject_meta(b)


def inject_meta(schema: dict) -> dict:
    props = schema.setdefault("properties", {})
    props.update(META_PROPS)
    req = list(schema.get("required", []))
    for k in META_REQUIRED:
        if k not in req:
            req.append(k)
    schema["required"] = req
    return schema


def validate_file(yaml_path: Path, schema_path: Path) -> list[str]:
    yaml_mod, Draft202012Validator = _import_deps()

    with schema_path.open(encoding="utf-8") as f:
        raw_schema = json.load(f)
    schema = merge_meta(raw_schema)

    with yaml_path.open(encoding="utf-8") as f:
        data = yaml_mod.safe_load(f)

    validator = Draft202012Validator(schema)
    errors = []
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        loc = ".".join(str(p) for p in err.path) or "(root)"
        errors.append(f"  {loc}: {err.message}")
    return errors


SCAN_EXCLUDED_DIRS = {
    "node_modules",
    ".venv",
    "venv",
    ".pnpm-store",
    ".git",
    ".next",
    "dist",
    "build",
    "coverage",
}


def _walk_workspace(workspace_root: Path):
    """Percorre o workspace com PODA de diretórios pesados.

    Não usar glob('**/...'): ele atravessa node_modules/.pnpm-store inteiros
    antes de qualquer filtro, o que trava o validador em projetos reais.
    os.walk permite remover diretórios excluídos da descida (dirnames[:]).
    """
    import os

    for dirpath, dirnames, filenames in os.walk(workspace_root):
        dirnames[:] = [d for d in dirnames if d not in SCAN_EXCLUDED_DIRS]
        for name in filenames:
            yield Path(dirpath) / name


def _gitignore_protects_env(content: str) -> bool:
    """Verifica padrão real de .env no .gitignore (linha .env, *.env ou .env*)."""
    import re

    patterns = (
        r"^\.env$",
        r"^\.env\*",
        r"^\*\.env$",
        r"^\*\.env\*",
        r"^\*\*/\.env$",
        r"^\*\*/\.env\*",
    )
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if any(re.match(pattern, stripped) for pattern in patterns):
            return True
    return False


def _scan_sensitive_files(workspace_root: Path) -> tuple[list[Path], list[Path]]:
    """Uma única passada (com poda) coletando .env e possíveis chaves privadas."""
    env_files: list[Path] = []
    key_files: list[Path] = []
    key_suffixes = (".pem", ".key", ".pkcs12", ".pfx")
    for path in _walk_workspace(workspace_root):
        name = path.name
        if name.startswith(".env"):
            if name.startswith(".env.example") or name.endswith(".example"):
                continue
            env_files.append(path)
        elif name.endswith(key_suffixes):
            key_files.append(path)
    return env_files, key_files


def check_security_leaks() -> list[str]:
    """Varre o workspace local buscando vulnerabilidades básicas de segurança e vazamento de segredos.

    Casos de teste manuais (resultado esperado):
    1. .env presente + sem .gitignore → ALERTA MÁXIMO por cada .env encontrado
    2. .env presente + .gitignore com só 'venv/' → ALERTA (padrão .env ausente)
    3. .env presente + .gitignore com '.env', '*.env' ou '.env*' → OK (sem alerta de .env)
    4. Sem .env no workspace → OK para .env (chaves privadas ainda são checadas)
    """
    warnings = []
    workspace_root = RUNTIME_DIR.parent.parent

    gitignore_path = workspace_root / ".gitignore"
    gitignore_exists = gitignore_path.exists()
    gitignore_content = (
        gitignore_path.read_text(encoding="utf-8") if gitignore_exists else ""
    )

    env_files, key_files = _scan_sensitive_files(workspace_root)
    if env_files:
        if not gitignore_exists:
            for env in env_files:
                rel = env.relative_to(workspace_root)
                warnings.append(
                    f"  [Host Guard] ALERTA MÁXIMO: '{rel}' existe e .gitignore AUSENTE — "
                    "risco de commit acidental de segredos!"
                )
        elif not _gitignore_protects_env(gitignore_content):
            for env in env_files:
                rel = env.relative_to(workspace_root)
                warnings.append(
                    f"  [Host Guard] '{rel}' encontrado, mas .gitignore não protege .env "
                    "(adicione linha '.env', '*.env' ou '.env*' — 'venv/' sozinho não basta)!"
                )

    for key_path in key_files:
        warnings.append(
            f"  [Host Guard] Possível chave privada/certificado exposto no workspace: "
            f"'{key_path.relative_to(workspace_root)}'"
        )

    return warnings


def main() -> int:
    targets = sys.argv[1:]
    if targets:
        mapping = {
            (t if t.endswith(".yaml") else f"{t}.yaml"): FILE_TO_SCHEMA.get(
                t if t.endswith(".yaml") else f"{t}.yaml"
            )
            for t in targets
        }
        mapping = {k: v for k, v in mapping.items() if v}
    else:
        mapping = FILE_TO_SCHEMA

    failed = passed = 0
    for yaml_name, schema_name in sorted(mapping.items()):
        yaml_path = RUNTIME_DIR / yaml_name
        schema_path = SCHEMA_DIR / schema_name
        if not yaml_path.exists() or not schema_path.exists():
            print(f"SKIP {yaml_name}")
            continue
        errs = validate_file(yaml_path, schema_path)
        if errs:
            print(f"FAIL {yaml_name}")
            for e in errs:
                print(e)
            failed += 1
        else:
            print(f"OK   {yaml_name}")
            passed += 1

    # Executar validação de vazamentos de segredos (Host Guard)
    print("\n--- HOST GUARD & SECURITY AUDIT ---")
    sec_warnings = check_security_leaks()
    if sec_warnings:
        print("ALERT - Pendências de segurança detectadas:")
        for w in sec_warnings:
            print(w)
        # Não falha o build por aviso de segurança, mas exibe de forma clara
    else:
        print("OK    Nenhum segredo ou chave privada exposta no workspace.")

    print(f"\n{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

