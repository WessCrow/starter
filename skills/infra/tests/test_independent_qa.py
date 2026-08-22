"""Testes da seleção de contrato de entrega no QA independente."""
from __future__ import annotations

import importlib.util
from pathlib import Path

_SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "independent-qa.py"
_spec = importlib.util.spec_from_file_location("independent_qa", _SCRIPT_PATH)
independent_qa = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
assert _spec.loader is not None
_spec.loader.exec_module(independent_qa)  # type: ignore[union-attr]


def test_lite_usa_spec_quando_nao_ha_sprint_contract(tmp_path: Path):
    spec_path = tmp_path / "specs" / "001-lite" / "spec.md"
    spec_path.parent.mkdir(parents=True)
    spec_path.write_text("# Lite", encoding="utf-8")
    handoff = {
        "feature": {
            "sprint_contract_path": None,
            "spec_path": "specs/001-lite/spec.md",
        }
    }

    path, profile = independent_qa.resolve_delivery_contract(handoff, tmp_path)

    assert path == spec_path
    assert profile == "lite"


def test_full_tem_precedencia_quando_os_dois_paths_existem(tmp_path: Path):
    feature_dir = tmp_path / "specs" / "002-full"
    feature_dir.mkdir(parents=True)
    spec_path = feature_dir / "spec.md"
    contract_path = feature_dir / "sprint-contract.md"
    spec_path.write_text("# Spec", encoding="utf-8")
    contract_path.write_text("# Contrato", encoding="utf-8")
    handoff = {
        "feature": {
            "sprint_contract_path": "specs/002-full/sprint-contract.md",
            "spec_path": "specs/002-full/spec.md",
        }
    }

    path, profile = independent_qa.resolve_delivery_contract(handoff, tmp_path)

    assert path == contract_path
    assert profile == "full"
