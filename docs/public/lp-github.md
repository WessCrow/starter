<!-- lp-github.md = espelho do README.md (fonte). Sincronizar a cada edição do README. -->

# STARTER

Framework de regras para agentes de IA construírem software com método: kickoff guiado, contexto enxuto e validação obrigatória antes de qualquer "pronto".

![Runtime v5.4](https://img.shields.io/badge/Runtime-v5.4-blueviolet?style=flat-square)
![CI validate](https://github.com/WessCrow/starter/actions/workflows/validate.yml/badge.svg)
![QA Gate](https://img.shields.io/badge/QA_Gate-build_+_revisão-emerald?style=flat-square)
![AGENTS.md](https://img.shields.io/badge/Compatível-AGENTS.md-ff69b4?style=flat-square)

---

## O que é

Camada de governança entre o usuário e o agente. Não é boilerplate de código nem template visual. Compõe-se de:

- YAML de runtime validado (regras, contexto, stack, decisões); o agente carrega só o necessário por sessão.
- Skills funcionais (`.skill`) para kickoff, QA, design, debug e refactor.
- Protocolos de fluxo (`flows/`) que o agente segue.
- Validadores executáveis que reprovam estrutura inválida ou comando perigoso.

Quem dirige o projeto é o usuário. O framework impede o agente de inventar, pular etapa ou marcar feature como pronta sem o build passar.

---

## Como usar

```text
1. Copie skills/ + AGENTS.md para a pasta do projeto
2. No chat do editor, digite: "Começar projeto"
3. Responda até 4 perguntas e confirme
```

O agente infere a stack, monta `runtime/`, gera CONTEXT.md/PRD.md e prepara o primeiro `sprint-contract.md`.

---

## Garantias e mecanismos

| Garantia | Mecanismo executável |
|---|---|
| Kickoff em ≤4 perguntas, sem jargão | `flows/kickoff.md` + `project-starter.skill` |
| Validação de estrutura, 0 falhas obrigatório | `validate.py` contra 11 JSON Schemas |
| Roteamento por tipo de ação | `flows/action-router.md` + `action-router.skill` |
| QA Gate antes de declarar feature pronta | `qa-gate.skill` (5 dimensões, FAIL se contrato não cumprido) |
| Build obrigatório | `qa-smoke.skill` (`pnpm run build` ou `npm`) |
| E2E no browser (Fase 4) | `qa-playwright.skill` (CLI/chromium, spec gerada do contrato) |
| Host Guard com enforce | Hook `PreToolUse:Bash` → `host-guard.sh` |
| Spec-driven para nova feature | `flows/feature-flow.md` |
| Continuidade entre IDEs/sessões | `state.yaml` + `handoff.yaml` |

---

## O que não entrega

- Não é template Next.js; o scaffolding roda quando o agente decide.
- Não é design system pronto; `design-system-structure.skill` orienta, não gera componentes.
- Não substitui code review humano; o QA Gate reprova erro óbvio, não substitui senioridade.
- Não funciona offline puro; depende do agente do editor.

---

## Fluxo para features

```text
Pedido → spec.md → clarify (≤5 perguntas) → plan.md → tasks.md → analyze → contrato aprovado → código → QA Gate
```

Sem código antes do contrato aprovado, inclusive em features simples.

---

## Compatibilidade

| Editor | Status |
|---|---|
| Cursor, Claude Code, Antigravity | Nativo (lê `AGENTS.md`) |
| VSCode, Windsurf, Cline, Roo | Compatível via `AGENTS.md` |

Recursos automatizados (hooks, orquestração por tier) degradam para convenção manual onde o harness não os suporta; nada quebra. Stack padrão: Next.js + pnpm (ou React + Vite). No Windows, os scripts `.sh` exigem WSL ou Git Bash.

---

> Framework open-source mantido por **Wesley Alves**.
> [Portfólio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Use, estude, evolua. Mantenha os créditos originais.
>
> **Última atualização:** 2026-06-16
