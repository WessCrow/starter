# tasks.md — [Nome da Feature]

> **Feature:** NNN-[nome-kebab]
> **Baseado em:** `plan.md`
> **Criado em:** YYYY-MM-DD
> **Protocolo:** `skills/governance/feature-flow.md`

---

<!--
⚠️ REGRAS DESTE ARQUIVO:
- Toda tarefa tem PATH de arquivo explícito.
- Ordem respeita dependências: modelos → serviços → UI.
- [P] = paralelizável (não depende de tarefa anterior incompleta).
- Marcar [x] ao concluir, na própria implementação.
- Todo critério de aceite do spec.md deve ter tarefa aqui (verificado na fase Analyze).
-->

## Fase A — Fundação

| ✓ | # | Tarefa | Arquivo(s) | Depende de |
|---|---|--------|-----------|------------|
| [ ] | T1 | | `src/…` | — |
| [ ] | T2 [P] | | `src/…` | — |

**Checkpoint A:** [o que deve funcionar ao fim desta fase]

---

## Fase B — História H1: [nome]

| ✓ | # | Tarefa | Arquivo(s) | Depende de |
|---|---|--------|-----------|------------|
| [ ] | T3 | | `src/…` | T1 |
| [ ] | T4 [P] | | `src/…` | T1 |

**Checkpoint B:** [critério de aceite testável — qual item do spec.md cobre]

---

## Fase C — História H2: [nome]

| ✓ | # | Tarefa | Arquivo(s) | Depende de |
|---|---|--------|-----------|------------|
| [ ] | T5 | | `src/…` | T3 |

**Checkpoint C:** [critério de aceite testável]

---

## Rastreabilidade

| Critério do spec.md | Tarefas |
|---------------------|---------|
| 1 | T3, T4 |
| 2 | T5 |

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: YYYY-MM-DD
