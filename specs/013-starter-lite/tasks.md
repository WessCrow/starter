# tasks.md — Perfil Starter Lite

> **Feature:** 013-starter-lite
> **Baseado em:** `plan.md`
> **Criado em:** 2026-08-21
> **Protocolo:** `skills/flows/feature-flow.md`

---

## Fase A — RED e contrato de dados

| ✓ | # | Tarefa | Arquivo(s) | Verificação | Depende de |
|---|---|--------|------------|-------------|------------|
| [x] | T1 | Adicionar casos RED que provem: uma spec Lite aprovada sem plan/tasks deve passar; uma Lite não aprovada deve falhar; uma Full sem tasks continua falhando. Não alterar o validador nesta tarefa. | `skills/infra/tests/test_spec_coherence.py` | RED observado: os dois casos Lite falharam antes da implementação. | — |
| [x] | T2 [P] | Criar testes RED para coleta explícita de arquivos, rejeição de path fora do workspace, deduplicação e erro quando nenhum path é informado. | `skills/infra/tests/test_calculate_tokens.py` | RED observado: quatro falhas por APIs ainda inexistentes. | — |
| [x] | T3 | Adicionar `governance.profile` (`lite` ou `full`) ao contexto atual, template e schemas; tornar Lite o padrão da base e manter os espelhos idênticos. | `skills/core/runtime/context.yaml`, `skills/core/runtime/schema/context.schema.json`, `skills/templates/runtime/context.yaml`, `skills/templates/runtime/schema/context.schema.json` | `validate.py context.yaml` passou; schemas core/template são idênticos. | T1, T2 |

**Checkpoint A:** os REDs estão documentados e o runtime aceita apenas os dois perfis válidos.

## Fase B — Roteamento e documentação proporcional

| ✓ | # | Tarefa | Arquivo(s) | Verificação | Depende de |
|---|---|--------|------------|-------------|------------|
| [x] | T4 | Implementar a decisão Lite/Full no fluxo, no roteador e nos resumos do bootstrap. Lite deve usar somente spec, sempre pausar para aprovação humana e promover se qualquer limite objetivo falhar. | `AGENTS.md`, `skills/flows/feature-flow.md`, `skills/flows/action-router.md`, `skills/catalog/action-router.skill`, `skills/core/runtime/routes.yaml`, `skills/templates/runtime/routes.yaml`, `skills/templates/specs/spec-template.md` | Busca textual confirmou Lite/Full e aprovação humana; `validate.py routes.yaml` passou. | T3 |
| [x] | T5 | Criar a fonte de soluções agrupada por cluster e limitar o gate a cinco gatilhos, um cluster relevante e no máximo três candidatos; corrigir a regra de licença para exigir compatibilidade real. | `skills/catalog/solution-sources.yaml`, `skills/catalog/priority-matrix.skill` | YAML validado com 7 clusters e limite 3; `validate-skills.py` passou 53/53. | T3 |
| [x] | T6 | Registrar o RED comportamental real desta mudança e o GREEN do mesmo cenário nas skills substancialmente alteradas, sem ativar skill nova. | `skills/catalog/action-router.skill`, `skills/catalog/priority-matrix.skill` | Logs registram o RED real do fluxo Full universal e o GREEN spec + aprovação humana. | T4, T5 |

**Checkpoint B:** um pedido pequeno toma o caminho Lite; busca externa não roda fora dos cinco gatilhos.

## Fase C — Validação, QA e tokens

| ✓ | # | Tarefa | Arquivo(s) | Verificação | Depende de |
|---|---|--------|------------|-------------|------------|
| [x] | T7 | Fazer o validador reconhecer `Profile: Lite`, exigir aprovação humana e riscos/critérios, proibir documentação Full no Lite e manter as regras Full atuais. | `skills/infra/scripts/check-spec-coherence.py`, `skills/infra/tests/test_spec_coherence.py` | 9 testes de coerência passaram, incluindo Lite aprovado, pendente e inchado. | T4 |
| [x] | T8 | Fazer o QA usar `spec.md` aprovado como contrato no Lite e `sprint-contract.md` no Full, inclusive no runtime e verificador independente. | `skills/core/runtime/qa.yaml`, schemas/templates correspondentes, `skills/catalog/qa-gate.skill`, `skills/catalog/qa-playwright.skill`, `skills/flows/qa-protocol.md`, `skills/infra/scripts/independent-qa.py`, `skills/infra/tests/test_independent_qa.py` | 2 testes do resolver passaram; suíte combinada 11/11; contrato runtime renomeado para delivery. | T7 |
| [x] | T9 | Refatorar a medição para aceitar somente paths explícitos efetivamente carregados, validar fronteira do workspace, deduplicar e atualizar o handoff sem varrer todo o catálogo. Atualizar a instrução pós-sessão. | `skills/scripts/calculate_tokens.py`, `skills/infra/tests/test_calculate_tokens.py`, `AGENTS.md` | 4 testes passaram; execução com 3 paths registrou exatamente 3 arquivos e 4.804 tokens. | T2, T3 |
| [x] | T10 | Registrar que Headroom permanece sem integração e só pode ser reconsiderado após benchmark controle/tratamento com tokens, latência, qualidade e falhas. | `skills/core/runtime/decisions.yaml` | Decisão registrada; validação e ausência de import serão verificadas no QA final. | T5, T9 |

**Checkpoint C:** specs Lite e Full são validadas, QA usa a fonte correta e a métrica não infla o contexto.

## Fase D — Analyze e QA

| ✓ | # | Tarefa | Arquivo(s) | Verificação | Depende de |
|---|---|--------|------------|-------------|------------|
| [x] | T11 | Rodar validação de runtime, skills, coerência, testes Python, higiene e diff-check; corrigir somente falhas causadas por esta feature. | arquivos alterados nesta feature | 99 testes; sintaxe 3/3; runtime 11/11; skills 59/59; coerência 36/36; higiene e diff PASS. | T6, T7, T8, T9, T10 |
| [x] | T12 | Atualizar estado, handoff, feature ativa, marcar tarefas concluídas e gerar relatório QA; não declarar PASS sem as saídas da sessão. | `skills/core/runtime/state.yaml`, `skills/core/runtime/handoff.yaml`, `skills/core/runtime/active-feature.yaml`, `qa/reports/` | Runtime validado 11/11; feature 013 e relatório QA PASS sincronizados. | T11 |

**Checkpoint D:** QA cético concluído e runtime coerente.

## Rastreabilidade

| Critério do spec.md | Tarefas |
|---------------------|---------|
| 1 | T4, T6 |
| 2 | T4, T7 |
| 3 | T3, T4, T7 |
| 4 | T5 |
| 5 | T5 |
| 6 | T10 |
| 7 | T2, T9 |
| 8 | T7, T8, T11 |
| 9 | T3, T4, T7 |

## Teste do padrão

- [x] Cada tarefa informa path, alteração e verificação observável.
- [x] Dependências estão ordenadas; apenas os REDs independentes estão marcados `[P]`.
- [x] Toda decisão necessária está no spec ou no plan, não apenas no chat.

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: 2026-08-21
