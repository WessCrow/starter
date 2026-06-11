# tasks.md — [Nome da Feature]

> **Feature:** NNN-[nome-kebab]
> **Baseado em:** `plan.md`
> **Criado em:** YYYY-MM-DD
> **Protocolo:** `skills/governance/feature-flow.md`

---

<!--
⚠️ REGRAS DESTE ARQUIVO:
- PADRÃO "JÚNIOR SEM CONTEXTO": cada tarefa deve ser executável por uma sessão
  nova de IA (ou um dev júnior) SEM re-explicação. Se a tarefa precisa do
  histórico do chat para fazer sentido, ela está mal escrita.
- Toda tarefa tem: PATH de arquivo explícito + O QUE fazer + COMO VERIFICAR.
- "Como verificar" é um comando ou ação observável (e o resultado esperado),
  não "deve funcionar".
- Ordem respeita dependências: modelos → serviços → UI.
- [P] = paralelizável (não depende de tarefa anterior incompleta).
- Marcar [x] ao concluir, na própria implementação — só após rodar a verificação.
- Todo critério de aceite do spec.md deve ter tarefa aqui (verificado na fase Analyze).
-->

## Fase A — Fundação

| ✓ | # | Tarefa (o quê + detalhe suficiente p/ sessão nova) | Arquivo(s) | Como verificar | Depende de |
|---|---|----------------------------------------------------|-----------|----------------|------------|
| [ ] | T1 | | `src/…` | `pnpm …` → [resultado esperado] | — |
| [ ] | T2 [P] | | `src/…` | | — |

**Checkpoint A:** [o que deve funcionar ao fim desta fase + como observar]

---

## Fase B — História H1: [nome]

| ✓ | # | Tarefa (o quê + detalhe suficiente p/ sessão nova) | Arquivo(s) | Como verificar | Depende de |
|---|---|----------------------------------------------------|-----------|----------------|------------|
| [ ] | T3 | | `src/…` | | T1 |
| [ ] | T4 [P] | | `src/…` | | T1 |

**Checkpoint B:** [critério de aceite testável — qual item do spec.md cobre]

---

## Fase C — História H2: [nome]

| ✓ | # | Tarefa (o quê + detalhe suficiente p/ sessão nova) | Arquivo(s) | Como verificar | Depende de |
|---|---|----------------------------------------------------|-----------|----------------|------------|
| [ ] | T5 | | `src/…` | | T3 |

**Checkpoint C:** [critério de aceite testável]

---

## Rastreabilidade

| Critério do spec.md | Tarefas |
|---------------------|---------|
| 1 | T3, T4 |
| 2 | T5 |

---

## Teste do padrão (antes de aprovar este arquivo)

```
[ ] Uma sessão nova de IA conseguiria executar cada tarefa só com este arquivo
    + runtime/*.yaml + SPEC.md da feature? (sem o histórico deste chat)
[ ] Toda tarefa tem "Como verificar" com comando/ação + resultado esperado?
[ ] Nenhuma tarefa depende de decisão que só existe na conversa?
    (se sim → mover a decisão para plan.md ou decisions.yaml)
```

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: YYYY-MM-DD
