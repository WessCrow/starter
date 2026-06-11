# playwright-setup.md — Fase 4 (Playwright CLI no QA Gate)

> **Para:** construir sozinho, sem ser programador  
> **Modo:** CLI only — sem MCP, sem dependência de Cursor conectado  
> **Objetivo:** o agente roda testes automáticos no browser antes de você confirmar

---

## O que você ganha

- Tela branca detectada **antes** de chegar até você
- Relatório com o que foi clicado e o que falhou (português)
- Screenshots em `qa/reports/screenshots/` quando algo quebrar
- Dev server gerenciado automaticamente pelo Playwright — sem precisar subir manualmente

---

## Setup único (uma vez por projeto filho)

No terminal, dentro do projeto (não do STARTER):

```bash
pnpm add -D @playwright/test
pnpm exec playwright install chromium --with-deps
```

Adicionar ao `package.json` do projeto:

```json
"scripts": {
  "test:e2e": "playwright test --project=chromium"
}
```

Copiar `playwright.config.ts` do template para a raiz do projeto:

```bash
cp skills/_deferred/phase4-playwright/templates/playwright.config.ts.template playwright.config.ts
```

Ajustar `baseURL` conforme stack:
- **Next.js:** `http://localhost:3000`
- **Vite:** `http://localhost:5173`

---

## Como funciona o `webServer`

O Playwright sobe o dev server automaticamente antes dos testes e derruba depois. Se você já tiver o servidor rodando, ele reaproveitado (`reuseExistingServer: true`).

**Você não precisa fazer nada.** Só rodar:

```bash
pnpm run test:e2e
```

---

## Como os testes são gerados

O agente gera `tests/e2e/[feature].spec.ts` **junto com a entrega da feature**, traduzindo cada critério do `sprint-contract.md` em uma assertion. Você não escreve os testes.

Regras que o agente segue:
- 1 critério do contrato = 1 teste isolado
- Seletores: `getByRole` > `getByText` > `getByLabel` — nunca classe CSS
- Sem `waitForTimeout` — `toBeVisible()` já tem retry automático
- Critério vago no contrato → marcado como `manual` no relatório, não vira teste

---

## Quando o Playwright é pulado

| Situação | Comportamento |
|----------|---------------|
| Feature API-only (sem UI) | `playwright.required: false` no contrato → SKIP |
| Sem `package.json` | SKIP + teste manual 5 min |
| `@playwright/test` não instalado | FAIL com instrução de setup |

---

## Problemas comuns

| Problema | Solução |
|----------|---------|
| `pnpm exec playwright install` falha | Verificar Node 18+ · tentar `npx playwright install chromium` |
| Teste falha com "locator not found" | Seletor CSS quebrou — usar `getByRole`/`getByText` |
| `webServer` timeout | Aumentar `timeout` no config para 120_000 |
| Port já em uso | Config tem `reuseExistingServer: true` — reaproveita automaticamente |

---

## Ativar a Fase 4 no STARTER

```
Diga ao agente: "ativar Fase 4 Playwright"
```

O agente move os arquivos de `_deferred/phase4-playwright/` para os lugares certos e atualiza `runtime/qa.yaml`.

---

> **Autoria:** Wesley Alves · [Portfolio](https://wesscrow.github.io/meu-portfolio/) · Última atualização: 2026-06-11
