# Start.md — Orchestrator (Referência Completa)

> **Runtime:** usar `Start-ops.md` — compacto, sem overhead.  
> **Governança de capability:** `skills-governance.md` — o que está ativo, adiado e futuro.  
> **Este arquivo:** referência para entender o sistema. Não carregar em runtime.

---

---

## ⚡ Pré-execução — v5 Enterprise

```
1. skills/runtime/index.yaml              → hot/warm/cold
2. skills/runtime/validate.py             → 0 failed (se runtime editado)
3. Hot: rules.yaml, context.yaml, state.yaml
4. Warm: active-feature.yaml + SPEC.md    → se feature ativa
5. Warm: architecture.yaml               → sempre (decisões de infra antes de codar)
6. Cold: stack|decisions|routes           → sob demanda (index.yaml lazy)
7. Start-ops.md                           → orchestrator
   → sem runtime/: project-start.md → templates/runtime/
8. UI? → context.yaml#ds.components
```

> YAML validado por JSON Schema. CONTEXT.md = humano apenas.

---

## 🔭 Context Scoping — etapa obrigatória (V2)

> Protocolo completo: `governance/context-scoping.md`

```
[1] Identificar qual feature a tarefa toca
      ex: "adiciona botão delete na lista de clientes" → feature: customers

[2] Existe src/features/[feature]/SPEC.md?
      SIM → carregar SPEC.md da feature (entidades, fluxos, estado atual)
      NÃO → criar SPEC.md via templates/feature-spec-template.md antes de executar

[3] A tarefa exige domínio técnico específico?
      SIM → carregar skill correspondente (ver Roteamento por intenção abaixo)
      NÃO → não carregar skill — tarefa direta não precisa de overhead
```

**Regra de ouro:** `runtime/*.yaml` + SPEC.md (feature) = contexto suficiente para a IA.  
Se sentir necessidade de carregar mais → YAML desatualizado ou SPEC.md ausente.

**O que NUNCA vai no SPEC.md de feature:**  
`tokens` · `regras globais` · `componentes DS global` · `stack`  
Esses itens ficam em `runtime/rules.yaml`, `runtime/context.yaml`, `runtime/stack.yaml`.

---

## 🏗️ Projeto novo — detectar stack → executar structure skill

| Stack detectada | Skill |
|---|---|
| React + Vite / SPA / dashboard | `structure/react-vite-structure.skill` |
| Next.js / SSR / App Router | `structure/nextjs-structure.skill` |
| API / backend / microserviço | `structure/backend-structure.skill` |
| Monorepo / workspace / múltiplos apps | `structure/monorepo-structure.skill` |
| Design System / Storybook | `structure/design-system-structure.skill` |
| Clean Architecture / DDD / enterprise | `structure/clean-architecture.skill` |
| Frontend sem stack específica | `structure/frontend-structure.skill` |

Estrutura já existe no projeto? → pular esta camada.  
Sempre executar **antes** de qualquer skill funcional.

---

## 📦 Resolução de skills ativas — ordem fixa

```
1. structure/       → usar apenas em projeto novo / definição estrutural
2. local-skills/    → project-starter · qa-gate · qa-smoke · ux-audit
                       lenis-scroll · editorial-scroll-gallery · editorial-scroll-variants · sticky-scroll-gallery · cinematic-scroll-video-hero · cinematic-scroll-video-hero-frameworks · responsive-craft · emil-design-eng · prompt-library
                       figma-implement-design · figma-foundation-docs · figma-make · interface-design · web-design-cloner
                       visual-direction-brief · marketplace-curator
                       fluid-ui-review · fluid-ui-implementation · fluid-ui-snippets
                       context-cleaner · ux-diamond
                       hyperframes · hyperframes-cli · hyperframes-media
3. _deferred/       → incubação; não entra no roteamento ativo
4. linked-skills/ + skills.sh + cache
                    → capability futura; fora do fluxo operacional atual
```

**Regra:** se uma skill não estiver fisicamente disponível no repositório ativo, ela sai do roteamento até ser saneada.

---

## 🗺️ Roteamento por intenção

| Intenção | Skills prioritárias |
|---|---|
| Explorar problema, validar hipóteses antes de codar | `ux-diamond` |
| Direção visual / referências / estilo | `visual-direction-brief` → `web-design-cloner` → `interface-design` |
| Criar UI / componente / visual | `interface-design` → `web-design-cloner` → `emil-design-eng` → `responsive-craft` |
| Decompor site, screenshot ou referência concreta | `web-design-cloner` → `interface-design` |
| Revisar ou implementar fluidez, motion e microinterações | `fluid-ui-review` → `fluid-ui-implementation` → `fluid-ui-snippets` |
| Auditar UX / identificar problemas | `ux-audit` |
| Iniciar projeto novo | structure skill → `project-starter` |
| Nova feature em projeto existente (spec-driven) | `governance/feature-flow.md` → `templates/specs/` → `qa-gate` |
| Refatorar projeto existente | `ux-audit` → `interface-design` |
| Padrões web / boas práticas | `emil-design-eng` → `responsive-craft` |
| Documentação / kickoff | `project-starter` → `templates/` |
| Descobrir capability externa / marketplace / MCP | `marketplace-curator` |
| Implementar design Figma / Figma → código | `figma-implement-design` |
| Criar foundations no Figma / variables / text styles / página Foundation | `figma-foundation-docs` |
| Scroll suave / scroll-driven / parallax | `lenis-scroll` |
| Section editorial com scroll travado e fotos verticais | `editorial-scroll-gallery` → `responsive-craft` → `emil-design-eng` |
| Variacoes de scroll editorial / cards alternados / trilha dupla / parallax leve | `editorial-scroll-variants` → `editorial-scroll-gallery` → `responsive-craft` |
| Section sticky com troca de imagem por scroll | `sticky-scroll-gallery` → `lenis-scroll` → `responsive-craft` |
| Hero cinematografica com video scrub controlado por scroll | `cinematic-scroll-video-hero` → `responsive-craft` → `emil-design-eng` |
| Hero cinematografica com video scrub em React / Next / Vite | `cinematic-scroll-video-hero-frameworks` → `cinematic-scroll-video-hero` → `responsive-craft` |
| Layout responsivo / breakpoints / fluido | `responsive-craft` |
| Animação / micro-interação / polish de UI | `emil-design-eng` |
| Review de código de UI (before/after) | `emil-design-eng` |
| Estruturar / usar prompt de design | `prompt-library` → `governance/prompt-engineering.md` |
| Usar Figma Make / prompt-to-app / protótipo interativo | `figma-make` |
| Escrever / revisar microcopy, CTA, erro | `prompt-library` cat.2 → `guidelines/designer2627.md` |
| Pesquisa, entrevistas, hipóteses | `prompt-library` cat.1 |
| Crítica de fluxo, decisão, viés | `prompt-library` cat.3 → `ux-audit` |
| Brainstorm, desbloqueio, briefing | `prompt-library` cat.4 |
| Carreira, entrevista, feedback | `prompt-library` cat.5 |
| Vídeo em HTML / motion graphics / captions / transições | `hyperframes` |
| CLI do HyperFrames / preview / render / lint / inspect | `hyperframes-cli` |
| TTS / transcrição / remove-background para vídeo | `hyperframes-media` |
| Pós-implementação / gate de qualidade | `qa-gate` → `qa-smoke` |
| Nenhuma skill com score ≥ 2 | executar sem skill e registrar gap; não usar fallback remoto |

**Score:** 0 irrelevante · 1 secundária · 2 boa · 3 ideal  
**Regra:** 1 skill principal + máx. 2 secundárias (só se mudarem o resultado)  
**Modo:** Single (padrão) · Dual (estruturar + validar) · Pipeline (etapas dependentes)

**Fora do fluxo ativo nesta fase:** `linked-skills/`, `skills.sh` e `cache/`. Ver `skills-governance.md`.

---

## 📋 Checklist mental — preencher antes de executar

```
RULES.md lido?                sim / não → ler agora
CONTEXT.md (global) lido?     sim / não existe → project-start.md / não → ler agora
DS verificado?                sim / não aplicável

── Context Scoping (V2) ──────────────────────────────
feature identificada:         [feature]
SPEC.md existe?               sim → carregar / não → criar via feature-spec-template.md
SPEC.md contém item global?   não → ok / sim → mover para CONTEXT.md antes de prosseguir
──────────────────────────────────────────────────────

stack detectada:              [stack]
structure skill:              [skill] / já existe → pular

skill necessária?             sim → [skill] / não → executar sem skill
skill secundária:             [skill] / não necessária
modo:                         single / dual / pipeline

CONTEXT.md atualizar?         sim → atualizar ao final / não → justificar
SPEC.md da feature atualizar? sim → atualizar ao final / não → justificar
```

---

## 📤 Pós-execução — atualizar runtime ao final da sessão

**runtime/** (prioridade — fonte da IA):
- `state.yaml` — fase, last_work, next, blockers
- `decisions.yaml` — novas decisões
- `context.yaml` / `stack.yaml` — DS, stack, integrações
- `active-feature.yaml` — feature ativa

**CONTEXT.md humano** (resumo ≤50 linhas, se mudança visível ao time)

**SPEC.md da feature trabalhada** (toda sessão significativa):
- Estado atual: fase, último trabalho, próximo passo
- Novos componentes locais criados → seção Componentes
- Decisões locais tomadas → seção Decisões locais
- Armadilhas descobertas → seção Armadilhas

---

## 🚫 Nunca · ✅ Sempre

**Nunca**
- Executar sem `runtime/rules.yaml` e `runtime/context.yaml` carregados
- Tocar uma feature sem carregar o SPEC.md dela (ou criá-lo)
- Colocar token de DS, regra de código ou componente global dentro de um SPEC.md
- Criar componente sem verificar `context.yaml` → design_system
- Hardcode de cor, fonte ou espaçamento
- `any` em TypeScript · `console.log` em produção · imports/variáveis não usadas
- `<div>` onde existe elemento semântico HTML
- Tratar capability futura como capability ativa
- Estrutura de pastas improvisada sem structure skill
- Deixar SPEC.md desatualizado ao fim de sessão com mudança significativa

**Sempre**
- `runtime/*.yaml` + SPEC.md (feature) antes de executar
- Verificar DS em `runtime/context.yaml` antes de criar componente
- Criar SPEC.md via `feature-spec-template.md` se não existir
- 1 skill dominante — só carregar se o domínio técnico exigir
- Structure skill antes de skill funcional em projetos novos
- Atualizar SPEC.md da feature ao final de toda sessão significativa
- CONTEXT.md humano atualizado só para resumo visível ao time

---

> **Novo projeto:** structure skill → project-start.md → `templates/runtime/` → CONTEXT.md humano leve  
> **Feature existente:** runtime/*.yaml + SPEC.md → skill → atualizar runtime + SPEC.md  
> **Sem skill ativa adequada:** executar direto ou registrar gap; não usar fallback remoto nesta fase

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07
