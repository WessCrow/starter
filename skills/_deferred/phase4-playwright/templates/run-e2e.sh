#!/usr/bin/env bash
# STARTER QA Fase 4 — roda smoke E2E no projeto filho (não no meta STARTER)
# Uso: bash skills/infra/scripts/run-e2e.sh [feature-id]
set -euo pipefail

FEATURE="${1:-smoke}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

# 1. Verificar package.json
if [[ ! -f package.json ]]; then
  echo "SKIP: sem package.json — teste manual necessário"
  exit 0
fi

# 2. Verificar instalação do Playwright
if ! pnpm exec playwright --version &>/dev/null 2>&1; then
  echo "FAIL: @playwright/test não instalado."
  echo "  → pnpm add -D @playwright/test"
  echo "  → pnpm exec playwright install chromium --with-deps"
  exit 1
fi

# 3. Verificar spec da feature
SPEC="tests/e2e/${FEATURE}.spec.ts"
if [[ ! -f "$SPEC" ]]; then
  echo "WARN: $SPEC não encontrado — gerando a partir do sprint-contract..."
  echo "  → agente (executor Haiku) deve gerar o spec antes de rodar"
  exit 1
fi

# 4. Rodar só chromium, só o spec da feature
echo "→ Rodando: $SPEC (chromium)"
pnpm exec playwright test "$SPEC" --project=chromium --reporter=list

EXIT=$?

if [[ $EXIT -eq 0 ]]; then
  echo "✓ PASS — Playwright smoke ok"
else
  echo "✗ FAIL — colar log acima no relatório QA"
  echo "  Screenshots: qa/reports/playwright/"
fi

exit $EXIT
