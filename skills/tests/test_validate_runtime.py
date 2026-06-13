"""
Testes unitários para skills/runtime/validate.py.

Foco em:
- inject_meta / merge_meta: injeção de propriedades v/updated
- _gitignore_protects_env: regex de proteção .env
- validate_file: validação YAML contra schema JSON
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# Importar validate.py do runtime (não é pacote, precisa de path)
RUNTIME_DIR = Path(__file__).resolve().parents[1] / "runtime"
sys.path.insert(0, str(RUNTIME_DIR))
import validate as rv  # noqa: E402


# ---------------------------------------------------------------------------
# inject_meta / merge_meta
# ---------------------------------------------------------------------------

class TestInjectMeta:
    def test_adds_v_and_updated_to_properties(self):
        schema = {"type": "object", "properties": {}}
        result = rv.inject_meta(schema)
        assert "v" in result["properties"]
        assert "updated" in result["properties"]

    def test_adds_v_and_updated_to_required(self):
        schema = {"type": "object"}
        result = rv.inject_meta(schema)
        assert "v" in result["required"]
        assert "updated" in result["required"]

    def test_does_not_duplicate_required(self):
        schema = {"required": ["v", "updated"]}
        result = rv.inject_meta(schema)
        assert result["required"].count("v") == 1
        assert result["required"].count("updated") == 1

    def test_preserves_existing_required(self):
        schema = {"required": ["name"], "properties": {}}
        result = rv.inject_meta(schema)
        assert "name" in result["required"]


class TestMergeMeta:
    def test_removes_allof(self):
        schema = {"allOf": [{"$ref": "#/meta"}], "type": "object"}
        result = rv.merge_meta(schema)
        assert "allOf" not in result

    def test_removes_id(self):
        schema = {"$id": "some-id", "type": "object"}
        result = rv.merge_meta(schema)
        assert "$id" not in result

    def test_handles_oneof(self):
        schema = {
            "oneOf": [
                {"type": "object", "properties": {}},
                {"type": "object", "properties": {}},
            ]
        }
        result = rv.merge_meta(schema)
        assert "oneOf" in result
        for branch in result["oneOf"]:
            assert "v" in branch.get("properties", {})

    def test_does_not_mutate_original(self):
        original = {"type": "object", "properties": {"name": {}}}
        original_copy = json.loads(json.dumps(original))
        rv.merge_meta(original)
        assert original == original_copy


# ---------------------------------------------------------------------------
# _gitignore_protects_env
# ---------------------------------------------------------------------------

class TestGitignoreProtectsEnv:
    def test_dot_env_line_protects(self):
        assert rv._gitignore_protects_env(".env\n") is True

    def test_glob_star_env_protects(self):
        assert rv._gitignore_protects_env("*.env\n") is True

    def test_dot_env_star_protects(self):
        assert rv._gitignore_protects_env(".env*\n") is True

    def test_double_star_dot_env_protects(self):
        assert rv._gitignore_protects_env("**/.env\n") is True

    def test_venv_only_does_not_protect(self):
        assert rv._gitignore_protects_env("venv/\n.venv/\nnode_modules/\n") is False

    def test_comment_ignored(self):
        assert rv._gitignore_protects_env("# .env\nvenv/\n") is False

    def test_empty_gitignore_does_not_protect(self):
        assert rv._gitignore_protects_env("") is False

    def test_whitespace_only_does_not_protect(self):
        assert rv._gitignore_protects_env("   \n\n") is False


# ---------------------------------------------------------------------------
# validate_file — integração com schema JSON real
# ---------------------------------------------------------------------------

class TestValidateFile:
    def _write_yaml(self, path: Path, content: str) -> Path:
        path.write_text(content, encoding="utf-8")
        return path

    def _write_schema(self, path: Path) -> Path:
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
            },
            "required": ["name"],
        }
        path.write_text(json.dumps(schema), encoding="utf-8")
        return path

    def test_valid_yaml_passes(self, tmp_path: Path):
        yaml_path = self._write_yaml(tmp_path / "test.yaml", "v: '1.0'\nupdated: '2026-01-01'\nname: hello\n")
        schema_path = self._write_schema(tmp_path / "test.schema.json")
        errors = rv.validate_file(yaml_path, schema_path)
        assert errors == []

    def test_missing_required_field_fails(self, tmp_path: Path):
        yaml_path = self._write_yaml(tmp_path / "test.yaml", "v: '1.0'\nupdated: '2026-01-01'\n")
        schema_path = self._write_schema(tmp_path / "test.schema.json")
        errors = rv.validate_file(yaml_path, schema_path)
        assert len(errors) >= 1
        assert any("name" in e for e in errors)

    def test_wrong_type_fails(self, tmp_path: Path):
        yaml_path = self._write_yaml(tmp_path / "test.yaml", "v: '1.0'\nupdated: '2026-01-01'\nname: 123\n")
        schema_path = self._write_schema(tmp_path / "test.schema.json")
        errors = rv.validate_file(yaml_path, schema_path)
        assert len(errors) >= 1


# ---------------------------------------------------------------------------
# _yaml_get via merge_meta_branch (smoke)
# ---------------------------------------------------------------------------

class TestMergeMetaBranch:
    def test_returns_dict_with_meta(self):
        branch = {"type": "object", "properties": {}}
        result = rv.merge_meta_branch(branch)
        assert "v" in result["properties"]
        assert "updated" in result["properties"]

    def test_does_not_mutate_input(self):
        branch = {"type": "object"}
        original = dict(branch)
        rv.merge_meta_branch(branch)
        assert branch == original
