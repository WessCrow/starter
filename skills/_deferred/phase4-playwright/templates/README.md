# Templates QA — Fase 4 Playwright

Copiar pasta `qa/` para a **raiz do projeto filho** (app web).

```
projeto/
├── qa/
│   ├── e2e-scenario.yaml      ← de e2e-scenario.template.yaml
│   └── reports/
│       └── screenshots/
├── tests/e2e/
│   ├── playwright.config.ts   ← de playwright.config.ts.template
│   └── sprint-[feature].spec.ts
└── package.json               ← scripts test:e2e
```

## Setup rápido

1. `flows/playwright-setup.md` (Cursor MCP)  
2. `pnpm add -D @playwright/test && pnpm exec playwright install chromium`  
3. Preencher `qa/e2e-scenario.yaml`  
4. `pnpm run dev` em um terminal  
5. Rodar QA: `qa-gate` → `qa-playwright`

## Scripts package.json

```json
"test:e2e": "playwright test",
"test:e2e:report": "playwright show-report"
```

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07
