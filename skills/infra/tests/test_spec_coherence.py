"""
Testes de regressão para check-spec-coherence.py.

B3 (Sprint B) — "ligar no CI": o script já estava conectado em
.github/workflows/validate.yml e .githooks/pre-commit com --strict.
Estes testes codificam o "caso vermelho proposital" exigido pelo Done-when:
provam que o gate reprova specs incoerentes (spec↔plan↔tasks) e aprova
specs coerentes. Usam o parâmetro spec_roots para isolar do repo real.
"""
from __future__ import annotations

import importlib.util
import textwrap
from pathlib import Path

import pytest

_CSC_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check-spec-coherence.py"
_spec = importlib.util.spec_from_file_location("check_spec_coherence", _CSC_PATH)
csc = importlib.util.module_from_spec(_spec)  # type: ignore
_spec.loader.exec_module(csc)  # type: ignore


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_spec(root: Path, name: str, *, spec: str | None, plan: str | None, tasks: str | None) -> None:
    """Cria um diretório de spec NNN-* com os arquivos indicados."""
    d = root / name
    d.mkdir(parents=True)
    if spec is not None:
        (d / "spec.md").write_text(textwrap.dedent(spec), encoding="utf-8")
    if plan is not None:
        (d / "plan.md").write_text(textwrap.dedent(plan), encoding="utf-8")
    if tasks is not None:
        (d / "tasks.md").write_text(textwrap.dedent(tasks), encoding="utf-8")


_COHERENT_SPEC = """\
# Feature coerente
## Critérios de aceite
- O sistema deve fazer X
- O sistema deve fazer Y
## Análise de Riscos
- **Risco:** Risco A — Solução A
"""

_COHERENT_TASKS = """\
# Tasks

| Tarefa | Verificação |
|--------|-------------|
| [ ] Implementar X | teste unitário X |
| [ ] Implementar Y | teste unitário Y |
"""


# ---------------------------------------------------------------------------
# Caso VERMELHO proposital — gate deve reprovar
# ---------------------------------------------------------------------------

class TestRedCases:
    def test_criterios_sem_tasks_falha(self, tmp_path: Path):
        """spec.md com critérios, tasks.md sem nenhuma task → FAIL."""
        root = tmp_path / "specs"
        _make_spec(
            root, "099-broken",
            spec=_COHERENT_SPEC,
            plan="# Plano\n",
            tasks="# Tasks\n(nenhuma task com checkbox)\n",
        )
        _, errors = csc.check_spec_coherence(strict=True, spec_roots=[root])
        assert errors, "spec sem tasks deveria reprovar"

    def test_cobertura_insuficiente_falha(self, tmp_path: Path):
        """2 critérios mas só 1 task → cobertura insuficiente → FAIL."""
        root = tmp_path / "specs"
        _make_spec(
            root, "098-undercovered",
            spec=_COHERENT_SPEC,
            plan="# Plano\n",
            tasks="# Tasks\n- [ ] Só uma task\n",
        )
        _, errors = csc.check_spec_coherence(strict=True, spec_roots=[root])
        assert any("cobertura insuficiente" in e for e in errors)

    def test_tasks_sem_plan_em_strict_falha(self, tmp_path: Path):
        """tasks.md sem plan.md em modo --strict → FAIL (análise antes de execução)."""
        root = tmp_path / "specs"
        _make_spec(
            root, "097-noplan",
            spec=_COHERENT_SPEC,
            plan=None,
            tasks=_COHERENT_TASKS,
        )
        _, errors = csc.check_spec_coherence(strict=True, spec_roots=[root])
        assert any("plan.md AUSENTE" in e for e in errors)

    def test_tasks_sem_verificacao_falha(self, tmp_path: Path):
        """tasks com checkbox mas sem coluna/seção de Verificação → FAIL."""
        root = tmp_path / "specs"
        _make_spec(
            root, "096-noverif",
            spec=_COHERENT_SPEC,
            plan="# Plano\n",
            tasks="# Tasks\n- [ ] Implementar X\n- [ ] Implementar Y\n",
        )
        _, errors = csc.check_spec_coherence(strict=True, spec_roots=[root])
        assert any("sem Verificação" in e for e in errors)


# ---------------------------------------------------------------------------
# Caso VERDE — gate deve aprovar
# ---------------------------------------------------------------------------

class TestGreenCases:
    def test_spec_coerente_passa(self, tmp_path: Path):
        """spec + plan + tasks coerentes, com Verificação → sem erros."""
        root = tmp_path / "specs"
        _make_spec(
            root, "001-coerente",
            spec=_COHERENT_SPEC,
            plan="# Plano\n",
            tasks=_COHERENT_TASKS,
        )
        _, errors = csc.check_spec_coherence(strict=True, spec_roots=[root])
        assert errors == [], f"spec coerente não deveria reprovar: {errors}"

    def test_sem_specs_passa(self, tmp_path: Path):
        """Raiz sem diretórios de spec → OK (não falha)."""
        root = tmp_path / "specs"
        root.mkdir(parents=True)
        _, errors = csc.check_spec_coherence(strict=True, spec_roots=[root])
        assert errors == []
