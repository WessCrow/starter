#!/usr/bin/env bash
# patch-pnpm-workspace.sh — corrige ERR_PNPM_IGNORED_BUILDS (pnpm 11 + create-next-app)
# Uso: bash skills/scripts/patch-pnpm-workspace.sh [DIR]
# DIR = raiz do app com package.json (default: pwd). Ver governance/stack-guide.md

set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"

if [[ ! -f package.json ]]; then
  echo "SKIP: sem package.json em $(pwd)"
  exit 0
fi

cat > pnpm-workspace.yaml <<'EOF'
packages:
  - "."

onlyBuiltDependencies:
  - esbuild
  - "@swc/core"
  - sharp
  - unrs-resolver

verifyDepsBeforeRun: false
EOF

echo "OK: pnpm-workspace.yaml aplicado em $(pwd)"
