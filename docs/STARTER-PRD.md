# PRD — STARTER

> **Versão:** 1.0 · **Status:** Aprovado · **Atualizado:** 2026-05-20

## 1. Visão do Produto

**Problema:** Agentes perdem contexto entre sessões e violam padrões de código/design.

**Solução:** Runtime modular de skills com governança, YAML validado, QA Gate e kickoff "Começar projeto".

**Objetivo:** Trabalho consistente entre sessões e IDEs, com baixo consumo de tokens.

## 2. Usuários

- **Primária:** Agente de IA (sessões isoladas)
- **Secundária:** Product designer / builder solo (não dev)

## 3. Fora do escopo

- App de produção executável (é sistema operacional para agentes)
- Playwright Fase 4 ativo (deferred em `_deferred/phase4-playwright/`)

## 4. Features principais

- Runtime YAML + JSON Schema (`skills/runtime/`)
- QA Gate rígido (`qa-gate`, `qa-smoke`)
- Kickoff conversacional + limpeza automática de artefatos do framework
- Structure skills por stack
- Specialist Asks Protocol

> PRD completo histórico: expandir conforme evolução do framework.

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07
