"""
Testes unitários para as funções helper de validate-skills.py.

Ciclo TDD:
  RED  — testar comportamento esperado antes de confiar na função
  GREEN — função já implementada; confirmar que passa
  REFACTOR — cobrir edge cases
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Adiciona o diretório de scripts ao path para importar o módulo
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import validate_skills as vs  # noqa: E402  (import após path setup)


# ---------------------------------------------------------------------------
# parse_dot_list
# ---------------------------------------------------------------------------

class TestParseDotList:
    def test_single_item(self):
        assert vs.parse_dot_list("`qa-gate`") == ["qa-gate"]

    def test_multiple_items(self):
        result = vs.parse_dot_list("`qa-gate` · `qa-smoke` · `ux-audit`")
        assert result == ["qa-gate", "qa-smoke", "ux-audit"]

    def test_strips_backticks(self):
        assert vs.parse_dot_list("`foo`") == ["foo"]

    def test_empty_string(self):
        assert vs.parse_dot_list("") == []

    def test_only_separators(self):
        assert vs.parse_dot_list("· ·") == []


# ---------------------------------------------------------------------------
# extract_section
# ---------------------------------------------------------------------------

class TestExtractSection:
    def test_found(self):
        text = "BEFORE\n## Start\ncontent here\n## End\nAFTER"
        result = vs.extract_section(text, "## Start", "## End")
        assert "content here" in result
        assert "AFTER" not in result

    def test_start_not_found(self):
        assert vs.extract_section("abc", "MISSING", "END") == ""

    def test_end_not_found_returns_rest(self):
        text = "## Start\ncontent until eof"
        result = vs.extract_section(text, "## Start", "## Never")
        assert "content until eof" in result

    def test_empty_section(self):
        result = vs.extract_section("A## BCD", "## B", "CD")
        assert result == "## B"


# ---------------------------------------------------------------------------
# contains_any
# ---------------------------------------------------------------------------

class TestContainsAny:
    def test_found(self):
        assert vs.contains_any("hello world", ["world", "xyz"]) is True

    def test_not_found(self):
        assert vs.contains_any("hello world", ["abc", "xyz"]) is False

    def test_empty_snippets(self):
        assert vs.contains_any("hello", []) is False

    def test_empty_text(self):
        assert vs.contains_any("", ["abc"]) is False


# ---------------------------------------------------------------------------
# extract_local_links
# ---------------------------------------------------------------------------

class TestExtractLocalLinks:
    def test_extracts_local_links(self):
        text = "[doc](docs/guide.md) [other](../other.md)"
        links = vs.extract_local_links(text)
        assert "docs/guide.md" in links
        assert "../other.md" in links

    def test_ignores_http(self):
        text = "[ext](https://example.com)"
        assert vs.extract_local_links(text) == []

    def test_ignores_anchors(self):
        text = "[anchor](#section)"
        assert vs.extract_local_links(text) == []

    def test_strips_fragment(self):
        text = "[doc](guide.md#section)"
        links = vs.extract_local_links(text)
        assert "guide.md" in links

    def test_empty_text(self):
        assert vs.extract_local_links("") == []


# ---------------------------------------------------------------------------
# compare_exact
# ---------------------------------------------------------------------------

class TestCompareExact:
    def test_identical_files(self, tmp_path: Path):
        a = tmp_path / "a.txt"
        b = tmp_path / "b.txt"
        a.write_text("same content")
        b.write_text("same content")
        assert vs.compare_exact(a, b, "test") == []

    def test_different_files(self, tmp_path: Path):
        a = tmp_path / "a.txt"
        b = tmp_path / "b.txt"
        a.write_text("content A")
        b.write_text("content B")
        errors = vs.compare_exact(a, b, "test")
        assert len(errors) == 1
        assert "fora de sincronia" in errors[0]


# ---------------------------------------------------------------------------
# list_skill_stems
# ---------------------------------------------------------------------------

class TestListSkillStems:
    def test_finds_skills(self, tmp_path: Path):
        (tmp_path / "qa-gate.skill").write_text("# qa")
        (tmp_path / "qa-smoke.skill").write_text("# smoke")
        assert vs.list_skill_stems(tmp_path) == {"qa-gate", "qa-smoke"}

    def test_empty_directory(self, tmp_path: Path):
        assert vs.list_skill_stems(tmp_path) == set()

    def test_recursive(self, tmp_path: Path):
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "deep.skill").write_text("# deep")
        assert vs.list_skill_stems(tmp_path, recursive=True) == {"deep"}

    def test_non_recursive_ignores_subdirs(self, tmp_path: Path):
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "deep.skill").write_text("# deep")
        assert vs.list_skill_stems(tmp_path, recursive=False) == set()


# ---------------------------------------------------------------------------
# _yaml_get
# ---------------------------------------------------------------------------

class TestYamlGet:
    def test_nested_path(self):
        data = {"a": {"b": {"c": "value"}}}
        assert vs._yaml_get(data, ["a", "b", "c"]) == "value"

    def test_missing_key(self):
        assert vs._yaml_get({"a": 1}, ["a", "b"]) is None

    def test_empty_path(self):
        assert vs._yaml_get({"a": 1}, []) == {"a": 1}

    def test_none_data(self):
        assert vs._yaml_get(None, ["a"]) is None


# ---------------------------------------------------------------------------
# _check_start_local_resolution
# ---------------------------------------------------------------------------

class TestCheckStartLocalResolution:
    def test_pass_when_equal(self):
        start_text = "2. local-skills/ → `qa-gate` · `qa-smoke`\n3. other"
        passes, errors = vs._check_start_local_resolution({"qa-gate", "qa-smoke"}, start_text)
        assert errors == []
        assert any("start-local" in p for p in passes)

    def test_fail_missing_in_start(self):
        start_text = "2. local-skills/ → `qa-gate`\n3. other"
        _, errors = vs._check_start_local_resolution({"qa-gate", "qa-smoke"}, start_text)
        assert any("qa-smoke" in e for e in errors)

    def test_fail_extra_in_start(self):
        start_text = "2. local-skills/ → `qa-gate` · `ghost`\n3. other"
        _, errors = vs._check_start_local_resolution({"qa-gate"}, start_text)
        assert any("ghost" in e for e in errors)


# ---------------------------------------------------------------------------
# _check_fallback_snippets
# ---------------------------------------------------------------------------

class TestCheckFallbackSnippets:
    SAFE_TEXT = "This text has no fallback snippets."

    def test_pass_when_clean(self):
        passes, errors = vs._check_fallback_snippets(self.SAFE_TEXT, self.SAFE_TEXT)
        assert errors == []
        assert any("fallback" in p for p in passes)

    def test_fail_when_start_has_fallback(self):
        bad_text = "use `skills.sh` → cache → executar"
        _, errors = vs._check_fallback_snippets(bad_text, self.SAFE_TEXT)
        assert any("Start.md" in e for e in errors)

    def test_fail_when_project_start_has_fallback(self):
        bad_text = "use `skills.sh` → cache → executar"
        _, errors = vs._check_fallback_snippets(self.SAFE_TEXT, bad_text)
        assert any("project-start.md" in e for e in errors)


# ---------------------------------------------------------------------------
# _check_index_markers
# ---------------------------------------------------------------------------

class TestCheckIndexMarkers:
    VALID_INDEX = (
        "- **Ativas:** `structure/` + `local-skills/`\n"
        "- **Adiadas:** `_deferred/`\n"
        "- **Futuras:** `linked-skills/` + `cache/`\n"
    )

    def test_pass_all_present(self):
        passes, errors = vs._check_index_markers(self.VALID_INDEX)
        assert errors == []
        assert any("index" in p for p in passes)

    def test_fail_missing_ativas(self):
        text = "- **Adiadas:** `_deferred/`\n- **Futuras:** `linked-skills/` + `cache/`\n"
        _, errors = vs._check_index_markers(text)
        assert any("ativas" in e.lower() for e in errors)

    def test_fail_missing_adiadas(self):
        text = "- **Ativas:** `structure/` + `local-skills/`\n- **Futuras:** `linked-skills/` + `cache/`\n"
        _, errors = vs._check_index_markers(text)
        assert any("adiadas" in e.lower() for e in errors)


# ---------------------------------------------------------------------------
# _check_governance_snippets
# ---------------------------------------------------------------------------

class TestCheckGovernanceSnippets:
    FULL_GOVERNANCE = (
        "`skills/local-skills/*.skill`\n"
        "`skills/structure/*.skill`\n"
        "`skills/_deferred/**`\n"
        "`skills/linked-skills/`\n"
        "`skills/cache/`\n"
        "fallback por `skills.sh`\n"
    )

    def test_pass_all_present(self):
        passes, errors = vs._check_governance_snippets(self.FULL_GOVERNANCE)
        assert errors == []

    def test_fail_missing_snippet(self):
        text = "`skills/local-skills/*.skill`\n"
        _, errors = vs._check_governance_snippets(text)
        assert len(errors) >= 4


# ---------------------------------------------------------------------------
# Integração leve: validate_doc_runtime_sync com YAML temporário
# ---------------------------------------------------------------------------

class TestValidateDocRuntimeSync:
    def test_pass_when_yaml_active_and_doc_has_text(self, tmp_path: Path):
        """GREEN: yaml=active + doc contém 'Fase 4' → PASS."""
        import yaml as yaml_mod

        qa_yaml = tmp_path / "qa.yaml"
        qa_yaml.write_text(yaml_mod.dump({"phase_4_playwright": {"status": "active"}}))

        doc = tmp_path / "README.md"
        doc.write_text("Fase 4 Playwright ativa aqui.\n")

        original_pairs = vs._DOC_RUNTIME_SYNC_PAIRS[:]
        vs._DOC_RUNTIME_SYNC_PAIRS[:] = [{
            "id": "test_pair",
            "yaml_file": qa_yaml,
            "yaml_path": ["phase_4_playwright", "status"],
            "expected_yaml_value": "active",
            "doc_files": [doc],
            "required_text": "Fase 4",
            "forbidden_pattern": None,
        }]
        try:
            passes, errors = vs.validate_doc_runtime_sync()
            assert errors == []
            assert any("test_pair" in p for p in passes)
        finally:
            vs._DOC_RUNTIME_SYNC_PAIRS[:] = original_pairs

    def test_fail_when_yaml_active_but_doc_missing_text(self, tmp_path: Path):
        """RED scenario: yaml=active mas doc NÃO contém texto obrigatório → FAIL."""
        import yaml as yaml_mod

        qa_yaml = tmp_path / "qa.yaml"
        qa_yaml.write_text(yaml_mod.dump({"phase_4_playwright": {"status": "active"}}))

        doc = tmp_path / "README.md"
        doc.write_text("Sem menção alguma ao E2E aqui.\n")

        original_pairs = vs._DOC_RUNTIME_SYNC_PAIRS[:]
        vs._DOC_RUNTIME_SYNC_PAIRS[:] = [{
            "id": "test_fail",
            "yaml_file": qa_yaml,
            "yaml_path": ["phase_4_playwright", "status"],
            "expected_yaml_value": "active",
            "doc_files": [doc],
            "required_text": "Fase 4",
            "forbidden_pattern": None,
        }]
        try:
            _, errors = vs.validate_doc_runtime_sync()
            assert any("test_fail" in e for e in errors)
        finally:
            vs._DOC_RUNTIME_SYNC_PAIRS[:] = original_pairs

    def test_pass_when_yaml_not_active(self, tmp_path: Path):
        """GREEN: yaml=inactive → sem restrição no doc → PASS."""
        import yaml as yaml_mod

        qa_yaml = tmp_path / "qa.yaml"
        qa_yaml.write_text(yaml_mod.dump({"phase_4_playwright": {"status": "inactive"}}))

        doc = tmp_path / "README.md"
        doc.write_text("Nada sobre Fase 4.\n")

        original_pairs = vs._DOC_RUNTIME_SYNC_PAIRS[:]
        vs._DOC_RUNTIME_SYNC_PAIRS[:] = [{
            "id": "test_inactive",
            "yaml_file": qa_yaml,
            "yaml_path": ["phase_4_playwright", "status"],
            "expected_yaml_value": "active",
            "doc_files": [doc],
            "required_text": "Fase 4",
            "forbidden_pattern": None,
        }]
        try:
            passes, errors = vs.validate_doc_runtime_sync()
            assert errors == []
            assert any("inactive" in p for p in passes)
        finally:
            vs._DOC_RUNTIME_SYNC_PAIRS[:] = original_pairs
