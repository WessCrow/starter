# activate-phase4.md — Roteiro de Ativação do Playwright

> **Gatilho:** usuário diz "ativar Fase 4 Playwright"  
> **Quem executa:** agente (orquestrador coordena, executor roda os shells)  
> **Pré-requisito:** projeto filho já tem `package.json` e build passando

---

## Passo 1 — Setup no projeto filho

```bash
pnpm add -D @playwright/test
pnpm exec playwright install chromium --with-deps
```

Adicionar ao `package.json` do projeto:

```json
"test:e2e": "playwright test --project=chromium"
```

---

## Passo 2 — Copiar config

```bash
cp skills/_deferred/phase4-playwright/templates/playwright.config.ts.template playwright.config.ts
```

Ajustar `BASE_URL` conforme stack:
- Next.js → `http://localhost:3000`
- Vite → `http://localhost:5173`

Criar pasta de testes:

```bash
mkdir -p tests/e2e qa/reports/playwright
```

---

## Passo 3 — Ativar no runtime

Editar `skills/core/runtime/qa.yaml`:

```yaml
phase_4_playwright:
  status: active      # era: deferred
  enabled: true       # era: false
```

---

## Passo 4 — Mover skill para local-skills

```bash
cp skills/_deferred/phase4-playwright/qa-playwright.skill skills/catalog/qa-playwright.skill
```

Adicionar ao roteamento em `skills/flows/Start.md` — linha 2 da resolução:

```
`qa-playwright` ·
```

Adicionar ao `INDEX.md` na tabela de skills ativas:

```
| `qa-playwright.skill` | QA E2E browser (Fase 4) |
```

---

## Passo 5 — Validar

```bash
python3 skills/infra/scripts/validate-skills.py
```

Deve passar 21/0. Se falhar em `skill-catalog:start-local` → verificar se `qa-playwright` foi adicionado na linha 2 do Start.md.

---

## Passo 6 — Smoke test de verificação

Gerar spec mínimo para confirmar que o setup funciona:

```bash
bash skills/_deferred/phase4-playwright/templates/run-e2e.sh smoke
```

Se falhar com "spec não encontrado", criar `tests/e2e/smoke.spec.ts` manualmente:

```typescript
import { test, expect } from '@playwright/test';
test('página carrega', async ({ page }) => {
  await page.goto('/');
  await expect(page).not.toHaveTitle('');
});
```

PASS nesse teste = Fase 4 ativa e funcionando.

---

## Integração no QA Gate (pós-ativação)

O `qa-gate.skill` passa a incluir:

```
[3] qa-smoke (build) — igual a antes
[4] qa-playwright (executor Haiku):
      gerar spec se ausente → rodar → reportar PASS/FAIL
[5] relatório final
```

**Tier:** geração do spec e execução do shell → **executor (Haiku)**  
**Tier:** debug de falha obscura → **orquestrador (Sonnet/Opus)**

---

## Reverter (se precisar desativar)

```yaml
# qa.yaml
phase_4_playwright:
  status: deferred
  enabled: false
```

```bash
# mover skill de volta
mv skills/catalog/qa-playwright.skill skills/_deferred/phase4-playwright/
```

Remover `qa-playwright` da linha 2 do `Start.md` e do `INDEX.md`.  
Rodar `validate-skills.py` → 0 failed.

---

> **Autoria:** Wesley Alves · Última atualização: 2026-06-11
