# STARTER

**Um framework de regras para agentes de IA construírem projetos de software com método — kickoff guiado, contexto enxuto, validação obrigatória antes de qualquer "pronto".**

![Runtime v5.5](https://img.shields.io/badge/Runtime-v5.5-blueviolet?style=flat-square)
![CI validate](https://github.com/WessCrow/starter/actions/workflows/validate.yml/badge.svg)
![QA Gate](https://img.shields.io/badge/QA_Gate-build_+_revisão_cética-emerald?style=flat-square)
![AGENTS.md](https://img.shields.io/badge/Compatível-AGENTS.md-ff69b4?style=flat-square)

---

## O que é

STARTER é a **camada de governança** entre você e o agente. Não é boilerplate de código nem template visual. É um conjunto de:

- **YAML de runtime validado** (regras, contexto, stack, decisões) — agente carrega só o necessário por sessão
- **Skills funcionais** (`.skill`) para kickoff, QA, design, debug, refactor
- **Protocolos de fluxo** (`flows/`) que o agente segue, não sugestões
- **Validadores executáveis** que reprovam estrutura inválida ou comando perigoso

Quem dirige o projeto é você. O STARTER garante que o agente não invente, não pule etapa e não marque feature como pronta sem o build passar.

---

## Como usar (3 passos)

```text
1. Copie skills/ + AGENTS.md para a pasta do seu projeto
2. No chat do editor, diga: "Começar projeto"
3. Responda até 4 perguntas em português e confirme
```

O agente faz o resto: infere stack, monta `runtime/`, gera CONTEXT.md/PRD.md, prepara o primeiro `sprint-contract.md`.

---

## O que o STARTER **realmente** entrega

| Garantia | Mecanismo executável |
|---|---|
| **Kickoff em ≤4 perguntas, sem jargão técnico** | [`flows/kickoff.md`](skills/flows/kickoff.md) + [`project-starter.skill`](skills/catalog/project-starter.skill) |
| **Validação de estrutura — 0 failures obrigatório** | [`validate.py`](skills/core/runtime/validate.py) contra 11 JSON Schemas em `runtime/schema/` |
| **Roteamento por tipo de ação — contrato condicional + gate Figma** | [`flows/action-router.md`](skills/flows/action-router.md) + [`action-router.skill`](skills/catalog/action-router.skill) |
| **QA Gate cético antes de declarar feature pronta** | [`qa-gate.skill`](skills/catalog/qa-gate.skill) — pontua 5 dimensões, FAIL se contrato não cumprido |
| **Build obrigatório** | [`qa-smoke.skill`](skills/catalog/qa-smoke.skill) roda `pnpm run build` (ou `npm`) |
| **E2E real no browser (Fase 4)** | [`qa-playwright.skill`](skills/catalog/qa-playwright.skill) — CLI/chromium, spec gerada do contrato |
| **Host Guard com enforce real** | Hook `PreToolUse:Bash` → [`host-guard.sh`](skills/infra/scripts/host-guard.sh) bloqueia `rm -rf /`, pipe-to-shell, `~/.ssh`, install global, force push em `main` |
| **Spec-driven para nova feature** | [`flows/feature-flow.md`](skills/flows/feature-flow.md): specify → clarify → plan → tasks → analyze → implement |
| **Continuidade entre IDEs/sessões** | `state.yaml` + `handoff.yaml` como única fonte da verdade |
| **Economia de tokens e de tier** | `context-cleaner.skill` + orquestração por tier ([AGENTS.md §0g](AGENTS.md)) |
| **Retrospectiva pós-sprint para melhoria de regras** | [`retro-analyst.skill`](skills/catalog/retro-analyst.skill) — analisa commits e logs para sugerir evoluções do runtime |

---

## O que o STARTER **não** entrega

- ❌ Não é um template Next.js — você ainda precisa rodar `pnpm dlx create-next-app` ou similar quando o agente decidir
- ❌ Não é design system pronto — `structure/design-system-structure.skill` orienta, não gera componentes
- ❌ Não substitui code review humano — o QA Gate reprova bobagem óbvia, não substitui senioridade
- ❌ Não funciona offline puro — depende do agente do seu editor (Cursor, Claude Code, Antigravity, Cline, Roo, etc.)

---

## Stack suportado

Padrão: **Next.js + pnpm** · Alternativa rápida: **React + Vite + pnpm** · Backend: **estrutura modular agnóstica** (FastAPI/Express/etc).

A escolha é inferida do que você responde no kickoff — você não precisa nomear stack.

---

## Compatibilidade

| Editor | Status |
|---|---|
| Cursor, Claude Code, Antigravity | **Nativo** — lê `AGENTS.md` direto |
| VSCode, Windsurf, Cline, Roo | Compatível via `AGENTS.md` |

### Degradação graciosa por ambiente

O STARTER funciona em qualquer editor que leia `AGENTS.md`. Recursos automatizados (hooks, orquestração por tier) **degradam para convenção manual** onde o harness não os suporta — nada quebra, você só perde a automação. O que cada ambiente garante de fato:

| Editor / Harness | Lê `AGENTS.md` | Hook de sessão (§0f) | Orquestração por tier (§0g) |
|------------------|:--------------:|----------------------|------------------------------|
| **Cursor / Claude Code** | ✅ nativo | ✅ `SessionStart` automático | ✅ delega via Task/subagent |
| **Antigravity** | ✅ nativo | ⚠️ via protocolo (nova sessão) | ⚠️ fluxo auxiliar / nova sessão |
| **Cline / Roo** | ✅ leitura | ❌ sem hook → lê `AGENTS.md` | ✅ Plan/Architect → Act/Code (nativo) |
| **Windsurf / VSCode** | ✅ leitura | ❌ → lê `AGENTS.md` no início | ❌ single-session + `handoff.yaml` |

**Por sistema operacional:** macOS/Linux rodam os scripts `.sh` (validate, hooks, patch pnpm) nativamente — cobertura total. No **Windows**, os scripts exigem **WSL ou Git Bash**; sem eles, o framework continua válido por convenção (o agente lê `AGENTS.md` e segue os protocolos manualmente), apenas sem os scripts de hook/validação automáticos.

---

## Estrutura mínima

```text
seu-projeto/
├── AGENTS.md             ← contrato com o agente
└── skills/
    ├── core/runtime/     ← YAML validado (hot/warm/cold)
    ├── catalog/          ← 34 skills funcionais
    ├── flows/            ← protocolos obrigatórios
    ├── structure/        ← arquitetura por stack
    ├── templates/        ← boilerplates de spec/contract
    └── infra/            ← validadores + host-guard
```

Detalhes em [`skills/INDEX.md`](skills/INDEX.md) · [O que é o STARTER](docs/public/O-QUE-E-O-STARTER.md)

---

> **Autoria** — Framework open-source mantido por **Wesley Alves**.
> [Portfólio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Use, estude, evolua. Mantenha os créditos originais.
>
> 🔗 [Meu Portfólio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> _Sinta-se livre para usar, estudar e evoluir a ferramenta! Apenas pedimos que mantenha os créditos originais do criador._
>
> **Última atualização:** 2026-06-16
