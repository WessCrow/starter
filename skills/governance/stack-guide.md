# stack-guide.md — Stack para projetos disruptivos

> **Para:** quem constrói sozinho, sem ser programador  
> **Atualizado:** 2026-05-20 · **Runtime:** `runtime/stack.yaml`

---

## Recomendação oficial STARTER

| Cenário | Stack | Structure skill |
|---------|-------|-----------------|
| **Produto / startup / app completo** (padrão) | **Next.js** (App Router) + TypeScript + Tailwind + shadcn/ui | `nextjs-structure.skill` |
| **Ferramenta rápida / dashboard / SPA** sem SEO pesado | **React + Vite** + TypeScript + Tailwind + shadcn/ui | `react-vite-structure.skill` |
| **API / backend separado** | Node + FastAPI etc. | `backend-structure.skill` |

**Padrão quando você não souber:** use **Next.js** — é a stack mais usada em produtos novos (Vercel, SSR, rotas, API routes, deploy simples).

---

## Gerenciador de pacotes: pnpm (recomendado)

| | **pnpm** (recomendado) | **npm** (ok se já usa) |
|---|------------------------|------------------------|
| Velocidade | Mais rápido em projetos médios/grandes | Adequado |
| Disco | Economiza espaço (links) | Duplica mais |
| Ecossistema moderno | Padrão em monorepos, Turborepo, muitos templates 2025+ | Universal, você já conhece |
| Comandos | `pnpm install`, `pnpm run build` | `npm install`, `npm run build` |

**Decisão STARTER:** agentes devem **preferir pnpm** em projetos novos e documentar no `CONTEXT.md`. Se o projeto já usa `package-lock.json`, manter **npm** até migração explícita.

Instalação (uma vez no Mac):

```bash
npm install -g pnpm
```

---

## pnpm 11 — evitar travas em agentes e usuários leigos

O pnpm 11 exige aprovação explícita de scripts de build. **Não use** `pnpm approve-builds` — é interativo e trava agentes de IA.

**Solução:** incluir `pnpm-workspace.yaml` na raiz de todo projeto novo com pnpm:

```yaml
packages:
  - "."

onlyBuiltDependencies:
  - esbuild
  - "@swc/core"
  - sharp

verifyDepsBeforeRun: false
```

- `onlyBuiltDependencies` — lista pacotes que podem rodar scripts de install sem prompt
- `verifyDepsBeforeRun: false` — evita bloqueio em CI e em agentes

As structure skills (`nextjs-structure.skill`, `react-vite-structure.skill`) devem gerar este arquivo junto com `package.json`.

**Proibido:** `pnpm approve-builds` em fluxos automatizados ou kickoff.

---

## Stack “disruptiva” no sentido produto (não experimental)

Evitar stacks exóticas só por hype — **disruptivo = produto + UX + velocidade de iteração**.

| Incluir | Evitar no início |
|---------|------------------|
| TypeScript | Linguagem obscura sem comunidade |
| Tailwind + shadcn | 5 libs de UI competindo |
| TanStack Query (dados) | `fetch` solto em todo lugar |
| Zod (validação) | Validação manual repetida |

---

## Onde isso vive no projeto

- **IA:** `runtime/stack.yaml` no projeto filho  
- **Humano:** uma linha no `CONTEXT.md`  
- **QA:** `qa-smoke.skill` roda `pnpm run build` (+ lint/test se scripts existirem) conforme stack detectada

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07
