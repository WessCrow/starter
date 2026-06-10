#!/usr/bin/env bash
# STARTER QA Fase 4 — roda E2E CLI no projeto filho (não no meta STARTER)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f package.json ]]; then
  echo "SKIP: sem package.json — use MCP Playwright ou teste manual"
  exit 0
fi

if ! pnpm exec playwright --version &>/dev/null 2>&1 && ! npx playwright --version &>/dev/null 2>&1; then
  echo "FAIL: Playwright não instalado. Rode: pnpm add -D @playwright/test && pnpm exec playwright install chromium"
  exit 1
fi

if [[ -f qa/e2e-scenario.yaml ]]; then
  echo "Cenário: qa/e2e-scenario.yaml"
fi

if pnpm run test:e2e 2>/dev/null; then
  exit 0
fi

pnpm exec playwright test tests/e2e --reporter=list 2>/dev/null || npx playwright test tests/e2e --reporter=list
