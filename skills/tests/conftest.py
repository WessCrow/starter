"""
Fixtures compartilhadas para a suite de testes do STARTER.

Cada fixture cria um repo mínimo em tmp_path para isolar os testes do repo real.
"""
from __future__ import annotations

import shutil
import textwrap
from pathlib import Path

import pytest


@pytest.fixture()
def fake_repo(tmp_path: Path) -> Path:
    """Cria estrutura mínima de repo STARTER para testes unitários."""
    # Sentinel
    (tmp_path / ".starter-framework-repo").touch()

    # Docs
    (tmp_path / "docs" / "public").mkdir(parents=True)
    (tmp_path / "docs" / "private").mkdir(parents=True)
    (tmp_path / "docs" / "private" / "README.md").write_text("# private\n")
    (tmp_path / "README.md").write_text("# STARTER\n")
    (tmp_path / "AGENTS.md").write_text("# AGENTS\n")
    (tmp_path / "COMECAR-PROJETO.md").write_text("# comecar\n")

    # Skills skeleton
    skills = tmp_path / "skills"
    (skills / "governance").mkdir(parents=True)
    (skills / "local-skills").mkdir(parents=True)
    (skills / "structure").mkdir(parents=True)
    (skills / "_deferred").mkdir(parents=True)
    (skills / "linked-skills").mkdir(parents=True)
    (skills / "cache").mkdir(parents=True)
    (skills / "templates").mkdir(parents=True)
    (skills / "outputs").mkdir(parents=True)
    (skills / "scripts").mkdir(parents=True)
    (skills / "runtime").mkdir(parents=True)

    # Bootstrap script mínimo
    bootstrap = skills / "scripts" / "clean-framework-artifacts.sh"
    bootstrap.write_text(
        textwrap.dedent("""\
        #!/usr/bin/env bash
        set -euo pipefail
        # .starter-framework-repo
        rm -rf skills/runtime
        rm -rf skills/outputs
        echo "Mantido: skills/ (governance, templates, local-skills, …), AGENTS.md"
        """)
    )

    return tmp_path


@pytest.fixture()
def repo_with_git(fake_repo: Path) -> Path:
    """fake_repo com git init para testes que precisam de git."""
    import subprocess
    subprocess.run(["git", "init"], cwd=fake_repo, capture_output=True, check=False)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=fake_repo, capture_output=True, check=False)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=fake_repo, capture_output=True, check=False)
    subprocess.run(["git", "add", "-A"], cwd=fake_repo, capture_output=True, check=False)
    subprocess.run(["git", "commit", "-m", "init"], cwd=fake_repo, capture_output=True, check=False)
    return fake_repo
