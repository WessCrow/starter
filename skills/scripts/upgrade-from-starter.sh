#!/usr/bin/env bash
# upgrade-from-starter.sh — atualiza validate.py + schema/ em projeto filho
# Uso: bash skills/scripts/upgrade-from-starter.sh [caminho-do-projeto-filho]
# Padrão: diretório atual (.)
#
# Copia APENAS:
#   - skills/templates/runtime/validate.py → skills/runtime/validate.py
#   - skills/templates/runtime/schema/     → skills/runtime/schema/
# Nunca sobrescreve .yaml preenchidos (state, handoff, rules, etc.)

set -euo pipefail

AUTO_YES=false
if [[ "${1:-}" == "-y" ]]; then
  AUTO_YES=true
  shift
fi

TARGET="${1:-.}"
TARGET="$(cd "$TARGET" && pwd)"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STARTER_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

SRC_VALIDATE="$STARTER_ROOT/skills/templates/runtime/validate.py"
SRC_SCHEMA="$STARTER_ROOT/skills/templates/runtime/schema"
DST_RUNTIME="$TARGET/skills/runtime"
DST_VALIDATE="$DST_RUNTIME/validate.py"
DST_SCHEMA="$DST_RUNTIME/schema"

if [[ ! -f "$SRC_VALIDATE" ]]; then
  echo "ERRO: template não encontrado em $SRC_VALIDATE"
  echo "Execute a partir de um projeto com pasta skills/ do STARTER."
  exit 1
fi

if [[ ! -d "$DST_RUNTIME" ]]; then
  echo "ERRO: $DST_RUNTIME não existe — projeto filho precisa ter skills/runtime/"
  exit 1
fi

FRAMEWORK_V="$(grep -E '^framework_v:' "$STARTER_ROOT/skills/runtime/state.yaml" 2>/dev/null | awk '{print $2}' | tr -d '"' || echo "unknown")"

echo "=== STARTER upgrade-from-starter ==="
echo "Origem (templates): $STARTER_ROOT/skills/templates/runtime/"
echo "Destino:            $DST_RUNTIME"
echo "Framework version:  $FRAMEWORK_V"
echo ""

echo "--- Diff validate.py (template → filho) ---"
if [[ -f "$DST_VALIDATE" ]]; then
  diff -u "$DST_VALIDATE" "$SRC_VALIDATE" || true
else
  echo "(arquivo novo — filho ainda não tem validate.py)"
fi
echo ""

echo "--- Diff schema/ (resumo) ---"
if [[ -d "$DST_SCHEMA" ]]; then
  diff -rq "$DST_SCHEMA" "$SRC_SCHEMA" || true
else
  echo "(pasta nova — filho ainda não tem schema/)"
fi
echo ""

if [[ "$AUTO_YES" == "true" ]]; then
  CONFIRM="s"
else
  read -r -p "Aplicar upgrade? [s/N] " CONFIRM
fi
if [[ ! "$CONFIRM" =~ ^[sS]$ ]]; then
  echo "Cancelado."
  exit 0
fi

mkdir -p "$DST_SCHEMA"
cp "$SRC_VALIDATE" "$DST_VALIDATE"
cp -R "$SRC_SCHEMA/." "$DST_SCHEMA/"

# Atualizar framework_v no state.yaml do filho (se existir)
STATE_YAML="$DST_RUNTIME/state.yaml"
if [[ -f "$STATE_YAML" ]]; then
  if grep -q '^framework_v:' "$STATE_YAML"; then
    sed -i.bak "s/^framework_v:.*/framework_v: \"$FRAMEWORK_V\"/" "$STATE_YAML"
    rm -f "$STATE_YAML.bak"
  else
    echo "framework_v: \"$FRAMEWORK_V\"" >> "$STATE_YAML"
  fi
  echo "framework_v atualizado em state.yaml"
fi

echo ""
echo "Validando..."
if python3 "$DST_VALIDATE"; then
  echo ""
  echo "OK — upgrade aplicado. validate.py: 0 failed."
else
  echo ""
  echo "AVISO — validate.py reportou falhas. Revise os YAML do projeto filho."
  exit 1
fi
