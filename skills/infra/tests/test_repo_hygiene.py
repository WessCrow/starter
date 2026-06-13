"""
Testes unitários para check-repo-hygiene.py.

Ciclo TDD RED→GREEN: testa os predicados puro-função (sem git) e o check principal
com listas de paths sintéticas.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

# O módulo tem hífens no nome — importar via importlib
import importlib.util, importlib.machinery

_HYGIENE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check-repo-hygiene.py"
_spec = importlib.util.spec_from_file_location("check_repo_hygiene", _HYGIENE_PATH)
hygiene = importlib.util.module_from_spec(_spec)  # type: ignore
_spec.loader.exec_module(hygiene)  # type: ignore


# ---------------------------------------------------------------------------
# _matches_forbidden_glob
# ---------------------------------------------------------------------------

class TestMatchesForbiddenGlob:
    def test_qa_report_matches(self):
        assert hygiene._matches_forbidden_glob("qa/reports/2026-06-01-report.md") is True

    def test_nested_qa_report_matches(self):
        assert hygiene._matches_forbidden_glob("project/qa/reports/foo.md") is True

    def test_normal_file_no_match(self):
        assert hygiene._matches_forbidden_glob("docs/guide.md") is False

    def test_skills_outputs_no_match(self):
        # skills/outputs/ é proibido por FORBIDDEN_PREFIXES, não por glob
        assert hygiene._matches_forbidden_glob("skills/outputs/ARCHITECTURE.md") is False


# ---------------------------------------------------------------------------
# _matches_forbidden_name
# ---------------------------------------------------------------------------

class TestMatchesForbiddenName:
    def test_relatorio_matches(self):
        assert hygiene._matches_forbidden_name("relatorio-sprint.md") is True

    def test_relatorio_with_underscore_matches(self):
        assert hygiene._matches_forbidden_name("relatorio_sprint.md") is True

    def test_plano_acao_matches(self):
        assert hygiene._matches_forbidden_name("plano-acao-criticos.md") is True

    def test_diagnostico_matches(self):
        assert hygiene._matches_forbidden_name("diagnostico.md") is True

    def test_starter_context_matches(self):
        assert hygiene._matches_forbidden_name("STARTER-CONTEXT.md") is True

    def test_normal_file_no_match(self):
        assert hygiene._matches_forbidden_name("README.md") is False

    def test_allowed_in_template_prefix(self):
        assert hygiene._matches_forbidden_name("skills/templates/relatorio-template.md") is False

    def test_case_insensitive(self):
        assert hygiene._matches_forbidden_name("RELATORIO-TEST.md") is True


# ---------------------------------------------------------------------------
# check_tracked_files
# ---------------------------------------------------------------------------

class TestCheckTrackedFiles:
    def test_clean_paths_no_violations(self):
        paths = ["README.md", "skills/flows/qa-protocol.md", "AGENTS.md"]
        assert hygiene.check_tracked_files(paths) == []

    def test_lab_path_violation(self):
        violations = hygiene.check_tracked_files(["_lab/pilot/index.ts"])
        assert len(violations) == 1
        assert "_lab/" in violations[0]

    def test_skills_outputs_violation(self):
        paths = ["skills/outputs/random-output.md"]
        violations = hygiene.check_tracked_files(paths)
        assert len(violations) == 1

    def test_allowed_in_forbidden_passes(self):
        # skills/outputs/ARCHITECTURE.md está em ALLOWED_IN_FORBIDDEN
        paths = ["skills/outputs/ARCHITECTURE.md"]
        assert hygiene.check_tracked_files(paths) == []

    def test_qa_report_violation(self):
        paths = ["qa/reports/2026-06-01.md"]
        violations = hygiene.check_tracked_files(paths)
        assert len(violations) == 1

    def test_forbidden_name_violation(self):
        paths = ["docs/private/relatorio-sprint.md"]
        violations = hygiene.check_tracked_files(paths)
        assert len(violations) == 1
        assert "relatorio-sprint.md" in violations[0]

    def test_empty_list(self):
        assert hygiene.check_tracked_files([]) == []

    def test_multiple_violations(self):
        paths = [
            "_lab/foo.ts",
            "qa/reports/rep.md",
            "README.md",  # OK
        ]
        violations = hygiene.check_tracked_files(paths)
        assert len(violations) == 2

    def test_docs_private_readme_allowed(self):
        # docs/private/README.md não é prefixo proibido per se
        # mas _matches_forbidden_name("README.md") = False → sem violação
        assert hygiene.check_tracked_files(["docs/private/README.md"]) == []
