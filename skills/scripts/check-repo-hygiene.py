#!/usr/bin/env python3
"""
STARTER Repo Hygiene Checker — detecta arquivos que não devem ser versionados.

Uso:
  python3 skills/scripts/check-repo-hygiene.py
  python3 skills/scripts/check-repo-hygiene.py --staged   # só o que vai no próximo commit

Política: skills/governance/repo-hygiene.md
"""

from __future__ import annotations

import fnmatch
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Caminhos/prefixos proibidos no índice git (exceto exceções explícitas)
FORBIDDEN_PREFIXES = (
    "_lab/",
    "skills/outputs/",
)

FORBIDDEN_GLOBS = (
    "qa/reports/*",
    "**/qa/reports/*",
)

# Exceções dentro de prefixos proibidos (relativo ao repo)
ALLOWED_IN_FORBIDDEN = {
    "docs/private/README.md",
}

# Padrões de nome — em qualquer pasta (exceto templates do framework)
FORBIDDEN_NAME_PATTERNS = (
    re.compile(r"^relatorio(-|_)", re.I),
    re.compile(r"^plano-(acao|melhoria)", re.I),
    re.compile(r"^diagnostico\.md$", re.I),
    re.compile(r"^STARTER-(PRD|CONTEXT)\.md$", re.I),
)

# Pastas onde padrões de nome são permitidos (artefatos de template)
NAME_PATTERN_ALLOW_PREFIXES = (
    "skills/templates/",
)


def _run_git(args: list[str]) -> list[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return []
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _git_tracked_files(staged_only: bool) -> list[str]:
    if staged_only:
        return _run_git(["diff", "--cached", "--name-only", "--diff-filter=ACMR"])
    return _run_git(["ls-files"])


def _matches_forbidden_glob(path: str) -> bool:
    normalized = path.replace("\\", "/")
    for pattern in FORBIDDEN_GLOBS:
        if fnmatch.fnmatch(normalized, pattern):
            return True
    return False


def _matches_forbidden_name(path: str) -> bool:
    normalized = path.replace("\\", "/")
    for prefix in NAME_PATTERN_ALLOW_PREFIXES:
        if normalized.startswith(prefix):
            return False
    name = Path(normalized).name
    return any(p.search(name) for p in FORBIDDEN_NAME_PATTERNS)


def check_tracked_files(paths: list[str]) -> list[str]:
    violations: list[str] = []

    for raw in paths:
        path = raw.replace("\\", "/")
        if path in ALLOWED_IN_FORBIDDEN:
            continue

        for prefix in FORBIDDEN_PREFIXES:
            if path.startswith(prefix) or path == prefix.rstrip("/"):
                violations.append(
                    f"  [repo-hygiene] '{path}' — prefixo proibido '{prefix}' "
                    "(artefato local/teste; ver repo-hygiene.md)"
                )
                break
        else:
            if _matches_forbidden_glob(path):
                violations.append(
                    f"  [repo-hygiene] '{path}' — relatório QA local "
                    "(use qa/reports/ fora do git ou docs/private/)"
                )
            elif _matches_forbidden_name(path):
                violations.append(
                    f"  [repo-hygiene] '{path}' — documento interno "
                    "(mover para docs/private/)"
                )

    return violations


def check_workspace_leaks() -> list[str]:
    """Avisa sobre arquivos no disco em pastas que deveriam ser só locais."""
    warnings: list[str] = []

    private_dir = REPO_ROOT / "docs" / "private"
    if private_dir.exists():
        for item in private_dir.iterdir():
            if item.name == "README.md":
                continue
            if item.is_file():
                tracked = _run_git(["ls-files", "--", str(item.relative_to(REPO_ROOT))])
                if tracked:
                    warnings.append(
                        f"  [repo-hygiene] '{item.relative_to(REPO_ROOT)}' está versionado — "
                        "deve ficar só em docs/private/ (gitignored)"
                    )

    lab_dir = REPO_ROOT / "_lab"
    if lab_dir.exists() and any(lab_dir.iterdir()):
        tracked_lab = [p for p in _run_git(["ls-files", "_lab/"]) if p]
        if tracked_lab:
            warnings.append(
                f"  [repo-hygiene] _lab/ tem {len(tracked_lab)} arquivo(s) versionado(s) — "
                "remover do índice (fixture de teste local)"
            )

    return warnings


def main() -> int:
    staged_only = "--staged" in sys.argv
    scope = "staged" if staged_only else "tracked"

    paths = _git_tracked_files(staged_only)
    violations = check_tracked_files(paths)
    violations.extend(check_workspace_leaks())

    print(f"--- REPO HYGIENE CHECK ({scope}) ---")
    if violations:
        print("FAIL — arquivos que não devem ir ao repositório:")
        for v in violations:
            print(v)
        print("\nCorrija: git rm --cached <arquivo> && mover para docs/private/")
        print("Política: skills/governance/repo-hygiene.md")
        return 1

    print(f"OK    Nenhuma violação em {len(paths)} arquivo(s) {scope}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
