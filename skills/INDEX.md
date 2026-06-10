# INDEX — v5.1 Enterprise + QA Gate

> **2026-05-20** · Runtime OS · Schema Validation · Quality Gate

## Sessão (agente) — ordem mínima

```
1. runtime/index.yaml
2. runtime/ hot → rules, context, state
3. runtime/ warm → active-feature (se aplicável)
4. runtime/ cold → sob demanda
5. governance/Start-ops.md
6. validate.py (após editar runtime)
```

## Runtime OS

| Recurso | Path |
|---------|------|
| Ordem de carga | [`runtime/index.yaml`](runtime/index.yaml) |
| Validador | [`runtime/validate.py`](runtime/validate.py) |
| Schemas | [`runtime/schema/`](runtime/schema/) |
| Docs | [`runtime/schema/README.md`](runtime/schema/README.md) |

## QA Gate ★

| Recurso | Papel |
|---------|-------|
| [`governance/qa-protocol.md`](governance/qa-protocol.md) | Portaria de qualidade (leia primeiro) |
| [`governance/stack-guide.md`](governance/stack-guide.md) | Next.js + pnpm vs npm |
| [`runtime/qa.yaml`](runtime/qa.yaml) | Pesos, gate rígido |
| [`runtime/handoff.yaml`](runtime/handoff.yaml) | Retomada + status QA |
| [`local-skills/qa-gate.skill`](local-skills/qa-gate.skill) | Avaliador cético (obrigatório pós-implementação) |
| [`local-skills/qa-smoke.skill`](local-skills/qa-smoke.skill) | build/lint |
| [`templates/sprint-contract.md`](templates/sprint-contract.md) | Contrato antes de codar |
| [`templates/qa-report.md`](templates/qa-report.md) | Relatório PT-BR |

## Iniciar projeto (comando único)

| Recurso | Papel |
|---------|-------|
| [`../COMECAR-PROJETO.md`](../COMECAR-PROJETO.md) | **Você:** só diga "Começar projeto" |
| [`governance/kickoff.md`](governance/kickoff.md) | Agente: limpeza + 4 perguntas |
| [`governance/bootstrap-cleanup.md`](governance/bootstrap-cleanup.md) | Limpeza automática do framework |
| [`scripts/clean-framework-artifacts.sh`](scripts/clean-framework-artifacts.sh) | Script de limpeza |
| [`local-skills/project-starter.skill`](local-skills/project-starter.skill) | Execução após "sim" |

## Nova feature — fluxo spec-driven ★

| Recurso | Papel |
|---------|-------|
| [`governance/feature-flow.md`](governance/feature-flow.md) | Protocolo: specify → clarify → plan → tasks → analyze → implementar |
| [`templates/specs/spec-template.md`](templates/specs/spec-template.md) | O quê + por quê (sem stack) + Clarificações |
| [`templates/specs/plan-template.md`](templates/specs/plan-template.md) | Como: stack, dados, arquitetura + constitution check |
| [`templates/specs/tasks-template.md`](templates/specs/tasks-template.md) | Tarefas com dependências, `[P]` e rastreabilidade |
| [`templates/overrides/README.md`](templates/overrides/README.md) | Customização de templates por projeto (override vence core) |

## Governance

| Doc | Papel |
|-----|-------|
| [`Start-ops.md`](governance/Start-ops.md) | Runtime Orchestrator + fluxo QA |
| [`skills-governance.md`](governance/skills-governance.md) | Define capability ativa, adiada e futura |
| [`Start.md`](governance/Start.md) | Matriz de roteamento de skills |
| [`validate-skills.py`](scripts/validate-skills.py) | Validador antidrift de skills, docs, templates e bootstrap |
| [`runtime-protocol.md`](governance/runtime-protocol.md) | Protocolo v5 |
| [`RULES.md`](governance/RULES.md) | Humano (completo) |
| [`runtime/rules.yaml`](runtime/rules.yaml) | IA (hot, validado) |

## Templates novos projetos

[`templates/runtime/`](templates/runtime/) — YAML + `schema/` + `index.yaml`

## Skills

- **Ativas:** `structure/` + `local-skills/`
- **Adiadas:** `_deferred/`
- **Futuras:** `linked-skills/` + `cache/`
- Estrutura física: [`STRUCTURE.md`](STRUCTURE.md)
- Catálogo humano: [`README.md`](README.md)

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-09
