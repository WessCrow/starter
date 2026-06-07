#!/usr/bin/env bash
# Remove artefatos copiados do repositório STARTER (framework) antes do kickoff.
# Uso: bash skills/scripts/clean-framework-artifacts.sh
# Executar na raiz do projeto novo.

set -euo pipefail

# Raiz = onde o comando foi executado (projeto novo), não o repo STARTER
ROOT="$(pwd)"

if [[ -f "$ROOT/.starter-framework-repo" ]]; then
  echo "ABORT: repositório STARTER (framework). Não rodar aqui — só no projeto novo."
  exit 1
fi

cd "$ROOT"

removed=()

if [[ -f CONTEXT.md ]]; then
  rm -f CONTEXT.md
  removed+=("CONTEXT.md")
fi

if [[ -f PRD.md ]]; then
  rm -f PRD.md
  removed+=("PRD.md")
fi

if [[ -d skills/runtime ]]; then
  rm -rf skills/runtime
  removed+=("skills/runtime/")
fi

if [[ -d skills/outputs ]]; then
  rm -rf skills/outputs
  removed+=("skills/outputs/")
fi

if [[ ${#removed[@]} -eq 0 ]]; then
  echo "OK: nada do framework para limpar (já estava limpo)."
else
  echo "OK: removido — ${removed[*]}"
fi

echo "Mantido: skills/ (governance, templates, local-skills, …), AGENTS.md"
