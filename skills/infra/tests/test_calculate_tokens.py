"""Testes da medição explícita de contexto do STARTER."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

_SCRIPT_PATH = Path(__file__).resolve().parents[2] / "scripts" / "calculate_tokens.py"
_spec = importlib.util.spec_from_file_location("calculate_tokens", _SCRIPT_PATH)
calculate_tokens = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
assert _spec.loader is not None
_spec.loader.exec_module(calculate_tokens)  # type: ignore[union-attr]


def test_resolve_loaded_files_rejeita_lista_vazia(tmp_path: Path):
    with pytest.raises(ValueError, match="arquivo"):
        calculate_tokens.resolve_loaded_files(tmp_path, [])


def test_resolve_loaded_files_rejeita_path_fora_do_workspace(tmp_path: Path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    outside = tmp_path / "outside.md"
    outside.write_text("segredo", encoding="utf-8")

    with pytest.raises(ValueError, match="fora do workspace"):
        calculate_tokens.resolve_loaded_files(workspace, [str(outside)])


def test_resolve_loaded_files_deduplica_e_preserva_ordem(tmp_path: Path):
    first = tmp_path / "first.md"
    second = tmp_path / "second.md"
    first.write_text("primeiro", encoding="utf-8")
    second.write_text("segundo", encoding="utf-8")

    resolved = calculate_tokens.resolve_loaded_files(
        tmp_path,
        ["first.md", "first.md", "second.md"],
    )

    assert resolved == [first.resolve(), second.resolve()]


def test_build_context_metrics_conta_somente_arquivos_informados(tmp_path: Path):
    loaded = tmp_path / "loaded.md"
    ignored = tmp_path / "ignored.md"
    loaded.write_text("abcd" * 10, encoding="utf-8")
    ignored.write_text("x" * 10_000, encoding="utf-8")

    metrics = calculate_tokens.build_context_metrics(
        tmp_path,
        calculate_tokens.resolve_loaded_files(tmp_path, ["loaded.md"]),
        date_value="2026-08-21",
    )

    assert metrics["files_loaded"] == ["loaded.md"]
    assert metrics["files_loaded_count"] == 1
    assert metrics["estimated_tokens"] > 0
