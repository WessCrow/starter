"""Alias de importação para validate-skills.py (hífens não são válidos em nomes de módulo Python)."""
import importlib.util
import sys
from pathlib import Path

_path = Path(__file__).resolve().parent / "validate-skills.py"
_spec = importlib.util.spec_from_file_location("validate_skills", _path)
_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
# Registrar ANTES do exec para que imports internos resolvam corretamente
sys.modules.setdefault("validate_skills", _mod)
_spec.loader.exec_module(_mod)  # type: ignore[union-attr]

# Expor o namespace completo do módulo neste módulo
globals().update({k: getattr(_mod, k) for k in dir(_mod) if not k.startswith("__")})
