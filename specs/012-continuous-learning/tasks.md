# tasks.md — Aprendizado Contínuo (Double-Loop Learning)

> **Feature:** 012-continuous-learning
> **Baseado em:** `plan.md`
> **Criado em:** 2026-06-19
> **Protocolo:** `skills/flows/feature-flow.md`

---

## Fase A — Fundações e Documentos de Fluxo

| ✓ | # | Tarefa (o quê + detalhe suficiente p/ sessão nova) | Arquivo(s) | Verificação | Depende de |
|---|---|----------------------------------------------------|-----------|----------------|------------|
| [ ] | T1 | Criar o documento de fluxo `skills/flows/continuous-learning.md` detalhando as obrigações dos Loops 1, 2 e Evaluator | `skills/flows/continuous-learning.md` | O arquivo existe e possui referências ao Loop 1, Loop 2 e ao Evaluator | — |
| [ ] | T2 [P] | Criar o arquivo `skills/catalog/learn.skill` para documentar a capacidade de auto-aperfeiçoamento do agente | `skills/catalog/learn.skill` | O arquivo existe e segue a estrutura padrão de skills do STARTER | — |

**Checkpoint A:** Documentações de fluxo e capacidade integradas no repositório.

---

## Fase B — Implementação dos Scripts de Automação

| ✓ | # | Tarefa (o quê + detalhe suficiente p/ sessão nova) | Arquivo(s) | Verificação | Depende de |
|---|---|----------------------------------------------------|-----------|----------------|------------|
| [ ] | T3 | Criar `skills/infra/scripts/record_session.py` que lê o `handoff.yaml` e cria um trace básico de sessão em `qa/runs/` | `skills/infra/scripts/record_session.py` | Rodar `python3 skills/infra/scripts/record_session.py` e ver o arquivo gerado em `qa/runs/` | T1 |
| [ ] | T4 | Criar `skills/infra/scripts/continuous_learner.py` que lê os traces de `qa/runs/`, compara com o `git diff` e reporta divergências | `skills/infra/scripts/continuous_learner.py` | Rodar `python3 skills/infra/scripts/continuous_learner.py` e verificar logs de análise de diffs | T3 |

**Checkpoint B:** Scripts de automação operando e gerando traces e relatórios preliminares.

---

## Fase C — Validação e Encaixe de Sistema

| ✓ | # | Tarefa (o quê + detalhe suficiente p/ sessão nova) | Arquivo(s) | Verificação | Depende de |
|---|---|----------------------------------------------------|-----------|----------------|------------|
| [ ] | T5 | Modificar `skills/infra/scripts/validate-skills.py` para incluir a validação de `learn.skill` e seus fluxos associados | `skills/infra/scripts/validate-skills.py` | Rodar `python3 skills/infra/scripts/validate-skills.py` e obter 0 erros | T2, T4 |

**Checkpoint C:** O validador do sistema aceita e integra a nova funcionalidade de aprendizado contínuo sem ferir regras de orçamentos.

---

## Rastreabilidade

| Critério do spec.md | Tarefas |
|---------------------|---------|
| 1. Trace em `qa/runs/` | T3 |
| 2. Comparação com correções (Loop 2) | T4 |
| 3. Propor modificação na skill relevante | T4 |
| 4. Validação obrigatória | T5 |
| 5. Autonomy Dial | T1, T2 |

---

## Teste do padrão (antes de aprovar este arquivo)

```
[x] Uma sessão nova de IA conseguiria executar cada tarefa só com este arquivo
    + runtime/*.yaml + SPEC.md da feature? (sem o histórico deste chat)
[x] Toda tarefa tem "Como verificar" com comando/ação + resultado esperado?
[x] Nenhuma tarefa depende de decisão que só existe na conversa?
```

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: 2026-06-19
