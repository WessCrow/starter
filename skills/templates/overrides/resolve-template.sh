#!/usr/bin/env bash
# resolve-template.sh — resolução de templates do STARTER (override vence core)
#
# Implementa a ordem fixa documentada em templates/overrides/README.md:
#   1. skills/templates/overrides/<path>   (customização do projeto — prioridade)
#   2. skills/templates/<path>             (core STARTER — padrão)
# Usa o PRIMEIRO encontrado e imprime o caminho resolvido + a origem.
#
# Uso:  ./resolve-template.sh <path-relativo-ao-templates>
# Ex.:  ./resolve-template.sh sprint-contract.md
set -euo pipefail

REL="${1:?uso: resolve-template.sh <path relativo a skills/templates/>}"

# Raiz de skills/templates/ (este script vive em skills/templates/overrides/)
TPL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

OVERRIDE="$TPL_ROOT/overrides/$REL"
CORE="$TPL_ROOT/$REL"

if [[ -f "$OVERRIDE" ]]; then
  echo "ORIGEM: override"
  echo "PATH:   $OVERRIDE"
  exit 0
elif [[ -f "$CORE" ]]; then
  echo "ORIGEM: core"
  echo "PATH:   $CORE"
  exit 0
else
  echo "ERRO: template '$REL' não encontrado em overrides/ nem no core" >&2
  exit 1
fi
