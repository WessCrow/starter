# INDEX — STARTER v5.2 · Roteador de Skills

> Runtime OS · QA Gate · Última atualização: 2026-06-11

---

## Ordem de carregamento (agente)

```
1. runtime/index.yaml
2. runtime/ hot → rules, context, state
3. runtime/ warm → active-feature (se aplicável)
4. runtime/ cold → sob demanda
5. flows/Start-ops.md
6. validate.py (após editar runtime)
```

---

## Runtime OS

| Recurso | Path |
|---------|------|
| Ordem de carga | `runtime/index.yaml` |
| Validador | `runtime/validate.py` |
| Schemas | `runtime/schema/` |

---

## QA Gate ★

| Recurso | Papel |
|---------|-------|
| `flows/qa-protocol.md` | Portaria de qualidade |
| `runtime/qa.yaml` | Pesos + gate rígido |
| `runtime/handoff.yaml` | Retomada + status QA |
| `catalog/qa-gate.skill` | Avaliador cético (obrigatório pós-código) |
| `catalog/qa-smoke.skill` | build/lint/test |
| `catalog/qa-playwright.skill` | QA E2E browser (Fase 4) |
| `templates/sprint-contract.md` | Contrato antes de codar |

---

## Fluxo de sessão

```
index.yaml → validate.py → hot → warm? → cold? → Start-ops → skill → validate → persist
```

---

## Iniciar projeto

| Recurso | Papel |
|---------|-------|
| `../COMECAR-PROJETO.md` | Só diga "Começar projeto" |
| `flows/kickoff.md` | Limpeza + 4 perguntas |
| `catalog/project-starter.skill` | Execução após "sim" |
| `scripts/clean-framework-artifacts.sh` | Fase 0 automática |

---

## Nova feature — spec-driven ★

| Recurso | Papel |
|---------|-------|
| `flows/feature-flow.md` | specify → clarify → plan → tasks → analyze → implementar |
| `templates/specs/spec-template.md` | O quê + por quê |
| `templates/specs/plan-template.md` | Como: stack, dados, arquitetura |
| `templates/specs/tasks-template.md` | Tarefas com `[P]` e dependências |
| `templates/overrides/README.md` | Override de templates por projeto |

---

## Governance

| Doc | Papel |
|-----|-------|
| `flows/Start-ops.md` | Orchestrator + fluxo QA |
| `flows/Start.md` | Roteamento de skills |
| `flows/action-router.md` | Roteador por tipo de ação + gate de fidelidade Figma |
| `catalog/action-router.skill` | Turbo (Claude): classifica modo e impõe contrato condicional |
| `flows/skills-governance.md` | Capability ativa/adiada/futura |
| `flows/model-orchestration.md` | Orquestração por tier (opt-in) |
| `flows/RULES.md` | Regras invioláveis (referência humana) |
| `runtime/rules.yaml` | Regras IA (hot, validado) |
| `flows/feature-flow.md` | Fluxo spec-driven |
| `flows/repo-hygiene.md` | O que versionar |
| `flows/host-guard.md` | Modelo Host Guard (convenção + hook) |
| `scripts/validate-skills.py` | Antidrift |
| `scripts/check-repo-hygiene.py` | Bloqueia fixtures no índice git |
| `scripts/host-guard.sh` | Hook PreToolUse:Bash — bloqueia comandos perigosos |

---

## Estrutura de diretórios

```
skills/
├── core/runtime/          ★ YAML operacional (hot/warm/cold + schema/)
├── flows/       Protocolos e orchestrator
├── catalog/     Skills funcionais (.skill)
├── structure/        Arquitetura de pastas por stack
├── templates/        Boilerplates (runtime/ + specs/ + overrides/)
├── guidelines/       Padrões de design
├── outputs/          Docs humanos vivos (não versionar relatórios)
├── linked-skills/    Reservado — capability futura
├── cache/            Reservado — cache remoto futuro
└── _deferred/        Skills adiadas (ex: Playwright)
```

- **Ativas:** `structure/` + `catalog/`
- **Adiadas:** `_deferred/`
- **Futuras:** `linked-skills/` + `cache/`

---

## Skills ativas (`catalog/`)

| Skill | Domínio |
|-------|---------|
| `project-starter.skill` | Kickoff de projeto |
| `qa-gate.skill` | QA cético pós-implementação |
| `qa-smoke.skill` | Build/lint/test |
| `qa-playwright.skill` | QA E2E browser (Fase 4) |
| `verify-before-done.skill` | Evidência antes de afirmação |
| `context-cleaner.skill` | Resumo para nova sessão |
| `session-review.skill` | Auto-avaliação pós-sessão |
| `ux-diamond.skill` | Discovery duplo-diamante |
| `ux-audit.skill` | Auditoria de UX |
| `scroll-animation.skill` | Scroll-driven (Lenis, sticky, video) |
| `responsive-craft.skill` | Layout responsivo + breakpoints |
| `fluid-ui.skill` | Motion, gestos, reduced-motion |
| `emil-design-eng.skill` | Polish visual + review de UI |
| `interface-design.skill` | Criação e refinamento de interfaces |
| `visual-direction-brief.skill` | Brief visual objetivo |
| `web-design-cloner.skill` | Decomposição de designs web |
| `figma-implement-design.skill` | Figma → código |
| `figma-foundation-docs.skill` | Foundations + variables no Figma |
| `figma-make.skill` | Figma Make / prompt-to-app |
| `prompt-library.skill` | Biblioteca de prompts |
| `marketplace-curator.skill` | Curadoria de skills/MCPs |
| `product-vision.skill` | Estratégia, roadmap, KPIs |
| `storyboard-cinematic.skill` | Pré-produção visual |
| `aw-designer.skill` | UI experimental (Awwwards) |
| `hypothesis-investigation.skill` | Investigação por hipótese |
| `landing-conversion.skill` | Landing de alta conversão |
| `portfolio-storytelling.skill` | Portfólio narrativo |
| `hyperframes.skill` | Composições de vídeo HTML |
| `hyperframes-cli.skill` | CLI do HyperFrames |
| `hyperframes-media.skill` | TTS, transcrição, remoção de fundo |
| `discovery.skill` | Estruturação de problema e contexto |
| `shaping.skill` | De ideia aberta a direção concreta |
| `design-critique.skill` | Qualidade visual e coerência estética |
| `framing-doc.skill` | Raciocínio em documentação utilizável |

---

## Checklist de manutenção

- [ ] `flows/Start.md` sincronizado com skills disponíveis?
- [ ] `flows/skills-governance.md` reflete capability real?
- [ ] Novos arquivos em `catalog/` e `structure/` documentados neste INDEX?
- [ ] `python3 skills/infra/scripts/validate-skills.py` passa sem erro?
- [ ] Templates atualizados conforme evolução?

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-11
