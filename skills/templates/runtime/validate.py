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

    print(f"\n{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
