# Start.md — Orchestrator (Referência Completa)

> **Runtime:** usar `Start-ops.md` (compacto).  
> **Capability:** `skills-governance.md`.  
> **Este arquivo:** referência. Não carregar em runtime.

---

## Pré-execução — v5

```
1. skills/core/runtime/index.yaml              → hot/warm/cold
2. skills/core/runtime/validate.py             → 0 failed (se runtime editado)
3. Hot: rules.yaml, context.yaml, state.yaml
4. Warm: active-feature.yaml + SPEC.md    → se feature ativa
5. Warm: architecture.yaml
6. Cold: stack|decisions|routes           → sob demanda
7. Start-ops.md                           → orchestrator
```

---

## Context Scoping (obrigatório)

```
[1] Identificar feature que a tarefa toca
[2] SPEC.md da feature existe?
      SIM → carregar SPEC.md
      NÃO → criar via templates/feature-spec-template.md antes de executar
[3] Tarefa exige domínio técnico específico?
      SIM → carregar skill correspondente
      NÃO → executar direto (sem overhead de skill)
```

**Regra de ouro:** `runtime/*.yaml` + SPEC.md (feature) = contexto suficiente.  
**NUNCA em SPEC.md:** tokens · regras globais · componentes DS global · stack → ficam em `runtime/`.

---

## Projeto novo — structure skill

| Stack detectada | Skill |
|-----------------|-------|
| React + Vite / SPA / dashboard | `structure/react-vite-structure.skill` |
| Next.js / SSR / App Router | `structure/nextjs-structure.skill` |
| API / backend / microserviço | `structure/backend-structure.skill` |
| Monorepo / múltiplos apps | `structure/monorepo-structure.skill` |
| Design System / Storybook | `structure/design-system-structure.skill` |
| Clean Architecture / DDD | `structure/clean-architecture.skill` |
| Frontend sem stack específica | `structure/frontend-structure.skill` |

Estrutura já existe → pular. Sempre executar **antes** de skill funcional.

---

## Resolução de skills ativas — ordem fixa

```
1. structure/       → projeto novo / definição estrutural
2. catalog/    → `project-starter` · `qa-gate` · `qa-smoke` · `qa-playwright` · `verify-before-done` · `context-cleaner` · `session-review`
                       `ux-diamond` · `ux-audit` · `scroll-animation` · `responsive-craft` · `fluid-ui` · `emil-design-eng`
                       `interface-design` · `visual-direction-brief` · `web-design-cloner`
                       `figma-implement-design` · `figma-foundation-docs` · `figma-make`
                       `prompt-library` · `marketplace-curator`
                       `product-vision` · `storyboard-cinematic` · `aw-designer`
                       `hypothesis-investigation` · `landing-conversion` · `portfolio-storytelling`
                       `hyperframes` · `hyperframes-cli` · `hyperframes-media`
                       `discovery` · `shaping` · `design-critique` · `ux-audit` · `framing-doc`
3. _deferred/       → incubação; não entra no roteamento ativo
4. linked-skills/ + cache/ → capability futura; fora do fluxo atual
```

---

## Roteamento por intenção

| Intenção | Skills prioritárias |
|----------|---------------------|
| Explorar problema / validar hipóteses | `ux-diamond` |
| Direção visual / referências / estilo | `visual-direction-brief` → `web-design-cloner` → `interface-design` |
| UI experimental / Awwwards | `aw-designer` → `scroll-animation` · `fluid-ui` → `emil-design-eng` |
| Criar UI / componente (dentro de sistema) | `interface-design` → `web-design-cloner` → `emil-design-eng` |
| Landing page de conversão | `landing-conversion` → `aw-designer` ou `interface-design` |
| Portfólio / case / narrativa | `portfolio-storytelling` → `aw-designer` |
| Decompor site / referência | `web-design-cloner` → `interface-design` |
| Fluidez / motion / microinterações | `fluid-ui` |
| Auditoria UX | `ux-audit` |
| Iniciar projeto novo | structure skill → `project-starter` |
| Nova feature (spec-driven) | `flows/feature-flow.md` → `templates/specs/` → `qa-gate` |
| Refatorar projeto | `ux-audit` → `interface-design` |
| Padrões web / boas práticas | `emil-design-eng` → `responsive-craft` |
| Figma → código | `figma-implement-design` |
| Figma foundations / variables | `figma-foundation-docs` |
| Figma Make / prompt-to-app | `figma-make` |
| Scroll / parallax / sticky / video scrub | `scroll-animation` → `responsive-craft` |
| Layout responsivo / breakpoints | `responsive-craft` |
| Animation / polish de UI | `emil-design-eng` |
| Prompts de design / microcopy | `prompt-library` → `guidelines/designer2627.md` |
| Investigação por hipótese | `hypothesis-investigation` |
| Visão de produto / roadmap / KPIs | `product-vision` |
| Storyboard / cenas / prompt de imagem | `storyboard-cinematic` |
| Marketplace / MCPs | `marketplace-curator` |
| Vídeo em HTML / motion graphics | `hyperframes` |
| CLI HyperFrames | `hyperframes-cli` |
| TTS / transcrição / remove-bg | `hyperframes-media` |
| QA pós-implementação | `qa-gate` → `qa-smoke` |
| Afirmar "pronto/corrigido" | `verify-before-done` |
| Fim de atividade pesada | `session-review` |
| Bug / erro / build quebrado | `flows/debugging-protocol.md` → `verify-before-done` |
| Feedback / crítica do usuário | `flows/review-reception.md` |
| Criar / editar skill ou regra | `flows/skill-testing.md` (TDD RED→GREEN) |
| Avaliar skill candidata | `flows/skill-intake.md` |
| Economia de modelo / delegação | `flows/model-orchestration.md` (ver `AGENTS.md` §0g) |
| Sem skill com score ≥ 2 | executar sem skill; registrar gap |

**Score:** 0 irrelevante · 1 secundária · 2 boa · 3 ideal  
**Regra:** 1 principal + máx. 2 secundárias · **Modos:** Single / Dual / Pipeline

---

## Checklist antes de executar

```
RULES.md lido?                    sim / não → ler agora
CONTEXT.md lido?                  sim / não existe → project-start.md / não → ler
DS verificado?                    sim / não aplicável
feature identificada:             [feature]
SPEC.md existe?                   sim → carregar / não → criar
structure skill:                  [skill] / já existe → pular
skill necessária?                 sim → [skill] / não → direto
modo:                             single / dual / pipeline
CONTEXT.md atualizar ao final?    sim / não → justificar
SPEC.md atualizar ao final?       sim / não → justificar
```

---

## Pós-execução

**runtime/:** `state.yaml` · `decisions.yaml` · `context.yaml`/`stack.yaml` · `active-feature.yaml`  
**CONTEXT.md humano:** resumo ≤50 linhas, só se mudança visível ao time  
**SPEC.md da feature:** estado atual · componentes criados · decisões locais · armadilhas

---

## Nunca / Sempre

**Nunca:** executar sem `rules.yaml` + `context.yaml` · tocar feature sem SPEC.md · item global em SPEC.md · hardcode · `any` TS · `console.log` produção · `<div>` onde existe semântica · capability futura como ativa

**Sempre:** runtime + SPEC.md antes de executar · verificar DS antes de criar componente · criar SPEC.md se não existir · 1 skill dominante · structure skill em projetos novos · atualizar SPEC.md ao final de sessão significativa

---

> **Novo projeto:** structure skill → project-start.md → `templates/runtime/` → CONTEXT.md leve  
> **Feature existente:** runtime/*.yaml + SPEC.md → skill → atualizar runtime + SPEC.md  
> **Sem skill ativa:** executar direto ou registrar gap

---

> **Autoria:** Wesley Alves · [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · Última atualização: 2026-06-11
