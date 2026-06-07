# playwright-setup.md — Fase 4 (Playwright no QA Gate)

> **Para:** construir sozinho, sem ser programador  
> **Objetivo:** o agente **clica no seu app** como um usuário, antes de você testar

---

## O que você ganha

- Menos “parecia ok no código mas no browser quebrou”
- Relatório com **o que foi clicado** e **o que falhou** (português)
- Screenshots em `qa/reports/screenshots/` (projetos filhos)

---

## Passo 1 — Playwright MCP no Cursor (recomendado)

1. Abra **Cursor** → **Settings** → **MCP** → **Add new MCP Server**
2. Nome: `playwright`
3. Tipo: **command**
4. Comando: `npx @playwright/mcp@latest`

Ou copie o exemplo do STARTER para o seu usuário Cursor:

- Arquivo modelo: `mcp.playwright.example.json` (raiz do STARTER)
- Destino: `~/.cursor/mcp.json` ou `.cursor/mcp.json` no projeto — **mesclar** com MCPs existentes

Requisito: **Node.js 18+**

Documentação oficial: https://playwright.dev/docs/getting-started-mcp

---

## Passo 2 — Playwright CLI no projeto (fallback)

Quando o MCP não estiver disponível, o agente usa testes em `tests/e2e/`.

No **projeto filho** (não no STARTER meta):

```bash
pnpm add -D @playwright/test
pnpm exec playwright install chromium
```

Scripts sugeridos no `package.json`:

```json
"scripts": {
  "test:e2e": "playwright test",
  "test:e2e:ui": "playwright test --ui"
}
```

Templates em `skills/templates/qa/`.

---

## Passo 3 — Cenário E2E (traduz contrato da sprint)

Arquivo: `qa/e2e-scenario.yaml` (copiar de `templates/qa/e2e-scenario.template.yaml`)

Cada linha do sprint-contract vira um passo:

- abrir URL
- clicar botão
- ver texto na tela
- viewport mobile 375px

O agente executa via **qa-playwright.skill**.

---

## Passo 4 — Subir o app antes do QA

| Stack | URL típica | Comando |
|-------|------------|---------|
| Vite | http://localhost:5173 | `pnpm run dev` |
| Next.js | http://localhost:3000 | `pnpm run dev` |

**QA Playwright só roda com app no ar.** Se não subir → relatório marca `playwright: skipped` e você testa manual (5 min).

---

## Fluxo integrado (Fase 4)

```txt
sprint-contract → implementar → qa-smoke (build)
                → qa-playwright (MCP ou CLI)
                → qa-gate (relatório final)
                → você confirma no browser
```

---

## Problemas comuns

| Problema | Solução |
|----------|---------|
| MCP não aparece | Reiniciar Cursor; conferir Node 18+ |
| Página em branco | `pnpm run dev` rodando? URL certa no e2e-scenario? |
| Teste CLI falha | `pnpm exec playwright install chromium` |
| Não é app web | Marcar `playwright.required: false` no e2e-scenario |

---

## Referências STARTER

- `local-skills/qa-playwright.skill`
- `runtime/qa.yaml` → `playwright`
- `governance/qa-protocol.md`

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07
