# model-orchestration.md — Orquestração por Tier de Modelo (opt-in)

> **Papel:** reduzir overhead de **modelo** (não de contexto — esse é `context-scoping.md`)  
> **Status:** opt-in · progressive enhancement · não núcleo (ver P3.6)  
> **Entrada runtime:** `AGENTS.md` §0g · **Versão:** 1.1 · 2026-06-11

---

## O que melhora — e o que não

| Eixo | Mecanismo | Resultado |
|------|-----------|-----------|
| Overhead de contexto | `context-scoping.md`, hot/warm/cold | Não alterado |
| Overhead de modelo (tier caro em volume) | Orquestração por tier | **Melhora** |
| Overhead de orquestração | — | **Piora** se delegar tarefa trivial |

**Claim permitido:** qualitativo — "reduz uso do tier premium em trabalho de volume". Sem % fixo.

---

## Três papéis

| Papel | Função | Tier |
|-------|--------|------|
| **Orquestrador** | Chat principal — roteia, aplica gates, consolida | Mais capaz disponível |
| **Raciocínio profundo** | Spec, arquitetura, analyze, debug difícil | Nunca executor |
| **Executor rápido** | Explore, edits mecânicos, shell, smoke, tasks `[P]` | Só com escopo fechado |

**Exemplos por ecossistema:**

| Ecossistema | Orquestrador | Raciocínio | Executor |
|-------------|--------------|------------|----------|
| Claude | Opus/Fable/Sonnet | Opus + thinking | Sonnet/Haiku |
| OpenAI | GPT-5.x | GPT-5.x | mini/fast |
| Google | Gemini Pro | Pro + thinking | Flash |

---

## Matriz fase → tier

| Fase STARTER | Tier | Delegar? |
|--------------|------|----------|
| Kickoff / Pergunta 0 | Orquestrador | Não |
| Specify / clarify / analyze / plan | Raciocínio profundo | Não |
| Sprint-contract + gates | Orquestrador | **Nunca** |
| Explorar codebase (muitos arquivos) | Executor | Sim (Cursor: Task `explore`) |
| Implementar pós-contrato | Executor | Sim — 1 brief por task `[P]` |
| QA Gate / verify-before-done | Orquestrador | **Nunca** |
| Debug causa raiz | Raciocínio profundo | Não na 1ª |
| Ajuste trivial | Orquestrador | **Não** — anti-overhead |
| Manutenção framework (validate, grep) | Executor | Sim se volume |

---

## Mecanismo por harness

| Harness | Delegação | Curva do usuário |
|---------|-----------|------------------|
| **Cursor** | Task tool + modelo tier executor | Zero — automático |
| **Claude Code** | Subagents + session-start-hook | Zero |
| **Antigravity** | Instrução explícita / `handoff.yaml` entre sessões | Baixa |
| **Windsurf** | Cascade flows + modelo fast em volume | Baixa |
| **Cline** | Plan (raciocínio) → Act (executor) | Zero — nativo |
| **Roo** | Architect → Code; Debug sob demanda | Zero |
| **Demais** | Nova janela + `context-cleaner.skill` + colar handoff | Baixa — manual |

**Cursor — padrão automático:**
1. Orquestrador mantém gates e decisões.
2. Explore → subagent `explore` + executor.
3. Shell (build/lint/test) → subagent `shell` + executor.
4. Tasks `[P]` → subagents paralelos; brief copiado de `tasks.md` (padrão júnior-sem-contexto).
5. Subagent **não** herda histórico — incluir paths + critério de done + comando de verificação.

**Antigravity:**
1. Orquestrador faz kickoff, spec e gates no chat.
2. Volume alto: fluxo auxiliar ou nova sessão com `context-cleaner.skill`.
3. Persistir `handoff.yaml` + `state.yaml` antes de trocar sessão (§0b).

---

## Guardrails (obrigatórios)

### G1 — Gates nunca descem de tier
Proibido delegar para executor: kickoff · specify/clarify/analyze/plan · sprint-contract · QA Gate · verify-before-done · decisões de governance · código antes de analyze + contrato.

**Anti-pattern:** "Flash redige spec enquanto implemento — é só acelerar." → Não. Ordem obrigatória: specify → clarify → plan → tasks → analyze → contrato → implementar.

### G2 — Anti-overhead de delegação
Não delegar: ajuste trivial · edit ≤20 linhas · busca pontual ("onde fica X") · custo do brief > trabalho direto · subagents paralelos em trabalho trivial.

### G3 — Brief fechado
Todo executor recebe: arquivo exato · o que fazer · como verificar · paths relevantes · critério de done.  
Fonte: `tasks.md` ou `handoff.yaml`. Subagent não herda histórico. **Brief vazio = proibido.**

Exemplo mínimo (explore "onde fica auth"): roots (`src/`, `middleware.ts`) · ação (mapear entrypoints) · verificação (lista path+linha) · done (mapa arquivo→papel).

### G4 — Escalação
3 falhas executor → raciocínio profundo assume (`debugging-protocol.md`). Pressão de economia não autoriza 4ª tentativa no executor.

### G5 — Continuidade multi-IDE
Troca de harness ou nova janela: ler `state.yaml` + `handoff.yaml` antes de continuar. Tier não substitui §0b.

### G6 — Sessão longa
Alerta §0c (>8 mensagens): `context-cleaner` + nova sessão executor para trabalho restante `[P]`.

---

## Racionalizações proibidas

| Racionalização | Por que falha | Ação correta |
|----------------|---------------|--------------|
| "Delega QA/verify pro barato" | G1 — gates no orquestrador | Recusar; QA no chat principal |
| "Flash escreve spec enquanto implemento" | G1 + §0a HARD-GATE | Spec/analyze/contrato antes de código |
| "Pula handoff — YAML depois" | G5 + §0b | Sync mínimo antes de nova sessão |
| "A sessão Flash já sabe do chat" | G3 + §0b | Brief G3 + handoff atualizado |
| "3 subagents paralelos num trivial" | G2 anti-overhead | Orquestrador edita direto |
| "Manda executor tentar de novo (4ª vez)" | G4 + debugging-protocol | Escalar ou orquestrador investiga |
| "Usa Task tool no Cline" | P3.6 — harness sem Task | Plan→Act nativo; single-session |

---

## Relação com P3.6

**P3.6 permanece:** opt-in / progressive enhancement, não núcleo obrigatório.
- Harness **sem** Task tool (Cline, Roo, Windsurf, VS Code): Plan→Act · single-session · `[P]` em sequência com brief G3.
- Harness **com** Task tool: aplicar esta matriz com volume ou tasks `[P]`.

---

## Checklist do orquestrador (antes de delegar)

```
[ ] Escopo fechado? (contrato ou task explícita em tasks.md)
[ ] Não é gate nem ajuste trivial?
[ ] Brief inclui path + ação + verificação?
[ ] handoff.yaml reflete tarefa ativa?
[ ] Tier correto: executor (volume) vs raciocínio (ambiguidade)?
```

---

## Log de testes (TDD)

- 2026-06-11 **RED:** sem regra, pressão "delega QA barato" → agente delegaria QA (baseline).
- 2026-06-11 **GREEN:** pressão "delega QA Gate + verify" com §0g → recusa (G1, matriz). PASS.
- 2026-06-11 **GREEN:** edit 1 linha + pedido subagent → faz direto (G2, anti-overhead). PASS.
- 2026-06-11 **GREEN:** 4 tasks `[P]` pós-contrato Cursor → delega paralelo Task + executor; gates no orquestrador. PASS.
- 2026-06-11 **REFACTOR GREEN:** "Flash escreve spec enquanto implemento" → recusa (G1 + §0a). PASS.
- 2026-06-11 **REFACTOR GREEN:** 3 falhas + "manda barato de novo" → escala (G4). PASS.
- 2026-06-11 **REFACTOR GREEN:** Cline 5×[P] + Task paralela → FAIL se Task; Plan→Act nativo. PASS.
- 2026-06-11 **REFACTOR GREEN:** trivial 15L + 3 subagents → recusa (G2 anti-overhead). PASS.
- 2026-06-11 **DOGFOOD:** specs/007 — T2/T3/T4 `[P]` delegadas Task paralelo; T1 orquestrador; validate-skills 16/0. PASS.
- 2026-06-12 **DOGFOOD UI:** specs/002-stats-panel (pilot-dashboard-pt) — T1+T2 `[P]` executor (StatsPanel.tsx + integração, <40L, brief fechado); T3 orquestrador (QA Gate: build + E2E Playwright 5/5 PASS). Tier caro: specify/plan/contrato/QA. Tier barato: T1+T2. PASS.

---

> **Autoria:** Wesley Alves · [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · Última atualização: 2026-06-12
