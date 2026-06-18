# skills-governance.md — Decisão Operacional de Skills

> **Papel:** definir o que é capacidade real, adiada e futura no STARTER  
> **Status:** ativo desde 2026-05-26 · Sprint 6 concluída 2026-06-11  
> **Este documento prevalece** sobre descrições ambíguas em outros arquivos.

---

## Classes de capability

| Classe | Inclui | Regra |
|--------|--------|-------|
| **Ativa** | `skills/catalog/*.skill` · `skills/structure/*.skill` · docs em `flows/` | Entra no fluxo normal |
| **Adiada** | `skills/_deferred/**` | Não aparece como opção prioritária no roteamento |
| **Futura** | `skills/linked-skills/` · `skills/cache/` · fallback por `skills.sh` | Não é suporte operacional atual |

---

## Decisões específicas

| Item | Decisão |
|------|---------|
| `linked-skills/` | Reservado para symlinks futuros. Diretório vazio ≠ suporte existente. |
| `skills.sh` | Fallback remoto desligado. Pode ser citado como direção futura, não como fluxo confiável. |
| `cache/` | Não é fonte operacional. Cache vazio ≠ erro estrutural. |
| `_deferred/` | Incubação — não promover implicitamente a capability ativa. Exceção: subpasta `phase4-pw/` contém scripts E2E da Fase 4 (ativa via CLI, `test:e2e`). |

---

## Fonte da verdade por camada

| Camada | Arquivo principal | Função |
|--------|-------------------|--------|
| Execução runtime | `flows/Start-ops.md` | Orchestrator compacto da sessão |
| Roteamento de skills | `flows/Start.md` | Resolução de skill por intenção |
| Definição de capability | **Este arquivo** | O que está ativo/adiado/futuro |
| Regras de código | `runtime/rules.yaml` (hot) + `flows/RULES.md` (humano) | Critérios de aceite |

---

## Decisões P3 — Superpowers (2026-06-11)

| Decisão | Regra |
|---------|-------|
| P3.1 — TDD para skills | Toda skill nova passa pelo ciclo RED→GREEN→REFACTOR de `skill-testing.md` antes de entrar no roteamento |
| P3.2 — HARD-GATE anti-"simples" | Trivial exige declaração explícita + 4 critérios objetivos; na dúvida → fluxo completo |
| P3.3 — Padrão júnior sem contexto | Toda task em `tasks.md`: arquivo exato + o que fazer + como verificar |
| P3.4 — Verify-before-done | `catalog/verify-before-done.skill` ativa. Proibido "pronto" sem evidência. |
| P3.5 — Protocolos comportamentais | `debugging-protocol.md` (causa raiz antes de fix) + `review-reception.md` (verificar feedback antes de implementar) |
| P3.6 — Hook session-start (opt-in) | `scripts/session-start-hook.sh` → harnesses com suporte a hooks (Claude Code). Demais: via AGENTS.md. |
| P3.6 — Subagent-driven dev | **Não assimilado** como núcleo — depende de Task tool uniforme entre harnesses |
| §0g — Tier de modelo (opt-in) | `model-orchestration.md` + AGENTS.md §0g. Progressive enhancement, não núcleo. |

---

## Decisões P4 — Sprint 005–006 (2026-06-11)

### Skill intake — vereditos finais

| Skill | Veredito | Destino |
|-------|----------|---------|
| AWDesigner | ASSIMILAR (override mantenedor) | `catalog/aw-designer.skill` |
| Visão de Produto | ASSIMILAR | `catalog/product-vision.skill` |
| STORYMASTER | ASSIMILAR (enxugada) | `catalog/storyboard-cinematic.skill` |
| IGH Investigador | ASSIMILAR | `catalog/hypothesis-investigation.skill` |
| Conversion UX LP | ASSIMILAR | `catalog/landing-conversion.skill` |
| Storytelling portfólio | ASSIMILAR | `catalog/portfolio-storytelling.skill` |
| AI Creative Director | REJEITAR | Overlap + persona inflada |
| CopyLab | REJEITAR | Duplica `prompt-library` cat.2 |
| Agente IGH (versão original) | ADIAR | `_deferred/skill-intake-2026-06/` |

**Regra reforçada:** skill sem intenção descoberta no roteamento = não assimilar.

### Fixes bootstrap (Sprint 006 — dogfooding)

| Fix | Entrega |
|-----|---------|
| F1 pnpm build | `scripts/patch-pnpm-workspace.sh` + structure skills + `qa-smoke` retry |
| F2 validate × _lab | `_lab` em `SKIP_MARKDOWN_PARTS` do `validate-skills.py` |
| F3 runtime pós-Fase 0 | `bootstrap-cleanup.md` + `kickoff.md` — obrigar `project-start` [1] antes de codar |

**Aceite pilotos:** `pnpm run build` PASS em `_lab/pilot-landing-en` e `_lab/pilot-dashboard-pt` (evidência 2026-06-11).

---

## Decisões P5 — Sprint 008 (2026-06-18)

### Skill intake — web-quality-skills (addyosmani/web-quality-skills)

| Skill | Veredito | Destino |
|-------|----------|---------|
| `web-quality-audit` | ASSIMILAR | `catalog/web-quality-audit.skill` |
| `performance` | ASSIMILAR | `catalog/performance.skill` |
| `core-web-vitals` | ASSIMILAR | `catalog/core-web-vitals.skill` |
| `accessibility` | ASSIMILAR | `catalog/accessibility.skill` |
| `seo` | ASSIMILAR | `catalog/seo.skill` |
| `best-practices` | ASSIMILAR | `catalog/best-practices.skill` |

**Motivação:** gap crítico identificado no pilar Frontend Engineering (~30% de maturidade). Skills externas cobrem performance, a11y em código, Core Web Vitals e SEO técnico — áreas sem qualquer cobertura prévia no catalog.  
**Fonte:** MIT · Addy Osmani (Chrome DevTools) · 1.8k stars · [github.com/addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills)  
**Intenções registradas no Start.md:** auditoria web, performance, LCP/INP/CLS, WCAG, SEO, boas práticas frontend.

---

## Como adicionar nova skill

1. Criar `.skill` em `catalog/` (ou `structure/` se estrutural)
2. Ciclo TDD RED→GREEN em `flows/skill-testing.md`
3. Atualizar `flows/Start.md` com roteamento
4. Atualizar este arquivo se mudar capability ativa/adiada/futura
5. Adicionar linha no `INDEX.md`

**Capability remota:** só ativar com política explícita para `linked-skills/` + `cache/` + validação.

---

> **Autoria:** Wesley Alves · [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · Última atualização: 2026-06-11
