# tasks.md — Seção de Depoimentos

> **Feature:** 001-depoimentos
> **Baseado em:** `plan.md`
> **Criado em:** 2026-06-09
> **Protocolo:** `skills/governance/feature-flow.md`

---

## Fase A — Componente

| ✓ | # | Tarefa | Arquivo(s) | Depende de |
|---|---|--------|-----------|------------|
| [x] | T1 | Criar seção Depoimentos com 3 cards estáticos | `src/modules/landing/components/Depoimentos.tsx` | — |

**Checkpoint A:** Componente renderiza título + 3 depoimentos

---

## Fase B — Integração

| ✓ | # | Tarefa | Arquivo(s) | Depende de |
|---|---|--------|-----------|------------|
| [x] | T2 | Inserir Depoimentos entre ComoFunciona e CtaFinal | `src/pages/HomePage.tsx` | T1 |

**Checkpoint B:** Landing exibe seção na ordem correta (critério 1 do spec)

---

## Rastreabilidade

| Critério do spec.md | Tarefas |
|---------------------|---------|
| 1 — seção com 3 depoimentos | T1, T2 |
| 2 — nome + frase clara | T1 |
| 3 — mobile 375px coluna | T1 |
| 4 — build compila | qa-smoke |

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
