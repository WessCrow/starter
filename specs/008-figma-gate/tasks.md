# tasks.md — Figma Gate

> **Feature:** 008-figma-gate
> **Baseado em:** `plan.md`
> **Criado em:** 2026-06-21
> **Protocolo:** `skills/flows/feature-flow.md`

---

## Fase A — Criar a skill de governance

| ✓ | # | Tarefa | Arquivo(s) | Verificação | Depende de |
|---|---|--------|-----------|-------------|------------|
| [ ] | T1 | Criar o diretório `skills/governance/` e o arquivo `figma-gate.skill` com estrutura base: (a) frontmatter YAML com `name: figma-gate`, `description` e `triggers`; (b) seção de gatilhos listando o que conta como referência Figma (URL, screenshot, arquivo exportado, menção explícita); (c) regra de bloqueio explícita — nenhuma task `[P]` de UI pode iniciar sem confirmação | `skills/governance/figma-gate.skill` | `cat skills/governance/figma-gate.skill` retorna o arquivo com frontmatter, seção de gatilhos e regra de bloqueio presentes | — |
| [ ] | T6 | Completar `figma-gate.skill` com: (d) formato de declaração obrigatório com os 5 campos do spec (componentes, hierarquia, tokens, comportamentos, ambiguidades); (e) protocolo de confirmação — agente aguarda resposta explícita, sem inferir silêncio como "sim"; (f) seção `## TDD Log` vazia para preenchimento pós-teste | `skills/governance/figma-gate.skill` | `grep -c "TDD Log\|confirmação\|Componentes identificados" skills/governance/figma-gate.skill` retorna ≥ 3 | T1 |

**Checkpoint A:** Skill existe, abrível, contém todas as 6 seções obrigatórias.

---

## Fase B — Integrar no feature-flow.md

| ✓ | # | Tarefa | Arquivo(s) | Verificação | Depende de |
|---|---|--------|-----------|-------------|------------|
| [ ] | T2 | Editar `skills/flows/feature-flow.md`. Localizar a Fase 1 (SPECIFY) e adicionar, imediatamente após ela e antes da Fase 2 (CLARIFY), um bloco condicional nomeado `[1.5] FIGMA GATE`. O bloco deve: (a) declarar a condição de ativação ("se a feature tem referência Figma"); (b) referenciar `skills/governance/figma-gate.skill` por caminho completo; (c) afirmar que nenhuma task de UI pode ser iniciada antes da confirmação; (d) listar o que conta como referência Figma (URL, screenshot, arquivo exportado, menção explícita) | `skills/flows/feature-flow.md` | `grep -n "FIGMA GATE" skills/flows/feature-flow.md` retorna a linha com o bloco inserido; `grep "figma-gate.skill" skills/flows/feature-flow.md` retorna o caminho da skill | T1 |

**Checkpoint B:** feature-flow.md referencia o gate; grep confirma presença.

---

## Fase C — Atualizar o validador

| ✓ | # | Tarefa | Arquivo(s) | Verificação | Depende de |
|---|---|--------|-----------|-------------|------------|
| [ ] | T3 | Editar `skills/infra/scripts/validate-skills.py` (ou o path equivalente em `qa/`). Adicionar um check que: (a) verifica se `skills/governance/figma-gate.skill` existe; (b) se não existir, imprime mensagem clara: `"ERRO: skills/governance/figma-gate.skill ausente — Figma Gate obrigatório"`; (c) retorna exit code não-zero. O check deve ser inserido junto com os demais checks de skills obrigatórias, não no final do arquivo | `skills/infra/scripts/validate-skills.py` | Rodar `python3 skills/infra/scripts/validate-skills.py` com a skill presente → 0 erros. Renomear temporariamente a skill → script imprime a mensagem de ERRO esperada e retorna exit ≠ 0. Desfazer rename | T1 |

**Checkpoint C:** Validador passa com skill presente; falha com mensagem correta sem ela.

---

## Fase D — Atualizar INDEX.md

| ✓ | # | Tarefa | Arquivo(s) | Verificação | Depende de |
|---|---|--------|-----------|-------------|------------|
| [ ] | T4 [P] | Editar `skills/INDEX.md`. Adicionar uma nova seção `## Governance` (se não existir) com entrada para `figma-gate.skill`: path completo + descrição de uma linha resumindo o papel da skill | `skills/INDEX.md` | `grep -n "figma-gate" skills/INDEX.md` retorna a entrada na seção Governance | T1 |

**Checkpoint D:** INDEX.md lista figma-gate.skill em seção Governance.

---

## Fase E — TDD: RED → GREEN

| ✓ | # | Tarefa | Arquivo(s) | Verificação | Depende de |
|---|---|--------|-----------|-------------|------------|
| [ ] | T5 | Executar teste manual do gate: (a) abrir nova sessão do agente; (b) fornecer uma URL Figma fictícia junto com pedido de implementação; (c) verificar que o agente para, emite o bloco de declaração com os 5 campos e aguarda confirmação; (d) responder "confirma" e verificar que o agente prossegue; (e) em nova sessão, fornecer URL Figma e **não** confirmar — verificar que o agente não gera código. Documentar resultado (PASS/FAIL por critério) na seção `## TDD Log` de `figma-gate.skill` | `skills/governance/figma-gate.skill` (seção TDD Log) | Seção `## TDD Log` da skill preenchida com ciclo RED→GREEN e data | T1, T2, T3, T4 |

**Checkpoint E:** TDD Log documentado com todos os critérios do spec marcados PASS.

---

## Rastreabilidade spec → tasks

| Critério do spec | Tarefas |
|------------------|---------|
| 1. Agente sempre para e declara antes de codar | T1, T2 |
| 2. Declaração com 5 campos obrigatórios | T6 |
| 3. Agente não avança sem confirmação | T6, T5 |
| 4. `feature-flow.md` referencia a skill | T2 |
| 5. `validate-skills.py` detecta ausência | T3 |
| 6. `INDEX.md` lista em governance | T4 |

---

## Teste do padrão (antes de aprovar este arquivo)

```
[x] Uma sessão nova de IA conseguiria executar cada tarefa só com este arquivo
    + runtime/*.yaml + spec.md da feature? (sem o histórico deste chat)
[x] Toda tarefa tem "Como verificar" com comando/ação + resultado esperado?
[x] Nenhuma tarefa depende de decisão que só existe na conversa?
[x] Nenhuma task [P] de UI presente — sem implicação para o gate em si
```

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: 2026-06-21
