# feature-flow.md — Fluxo Spec-Driven por Feature

> **Papel:** Protocolo obrigatório para adicionar **novas features** a um projeto já iniciado
> **Gatilho:** "Nova feature" · "Adicionar feature" · "Quero uma nova funcionalidade"
> **Não usar para:** projeto novo (use `kickoff.md`) · ajuste trivial (ver critérios rígidos em "HARD-GATE" abaixo)
> **Inspiração:** ciclo specify → clarify → plan → tasks → analyze do [spec-kit (GitHub)](https://github.com/github/spec-kit), adaptado à governança STARTER

---

## 🚧 HARD-GATE — sem código antes de aprovação humana

**Não escrever código, não criar arquivo de implementação e não fazer scaffold antes do humano aprovar o artefato do perfil:** `spec.md` no Lite; `sprint-contract.md` no Full.

### Anti-pattern nomeado: "isso é simples demais para precisar de spec"

Essa frase (ou variações: "é só um botão", "o usuário está com pressa", "vou só desta vez") é a racionalização mais comum para pular o fluxo. Feature pequena passa pelo Lite; o `spec.md` pode ser curto, mas existe e é aprovado.

### Exceção de ajuste trivial — critérios rígidos (TODOS obrigatórios)

Um ajuste só é trivial se cumprir **todos** os itens:

```
[ ] ≤ ~20 linhas alteradas
[ ] Nenhuma entidade, rota, tabela ou estado novo
[ ] Nenhum comportamento novo visível ao usuário (correção/copy/estilo pontual)
[ ] O agente DECLAROU no chat: "Tratando como ajuste trivial porque [critérios]"
    e o usuário não objetou
```

Na dúvida entre trivial e feature → **é feature**. Pressa do usuário não reclassifica a tarefa.
Mesmo trivial: QA Gate continua obrigatório (`qa-gate` + `qa-smoke`).

> **Log de testes (TDD):** 2026-06-11 GREEN — subagent sob pressão ("vai direto no código, sem spec, preciso pra hoje") manteve o gate, nomeou o anti-pattern e classificou corretamente como feature. PASS. Relatório completo: `skills/outputs/skill-tests/2026-06-11-p3-green.md` (local, não versionado — `repo-hygiene.md`).

---

## 🎯 Objetivo

O kickoff cobre o **início** do projeto. Este protocolo cobre a **evolução**: toda feature começa pequena, mas cresce para Full quando risco ou complexidade verificável exigir.

Regra central herdada do spec-kit: **o spec define o quê (sem tecnologia); o plan define o como (com tecnologia)**.

---

## 📂 Estrutura por feature

Cada feature ganha uma pasta numerada. O perfil define o conteúdo:

```
specs/
  001-nome-da-feature/
    spec.md              ← sempre; único documento no Lite
    plan.md              ← somente Full
    tasks.md             ← somente Full
    sprint-contract.md   ← somente Full
```

- Numeração sequencial com 3 dígitos (`001`, `002`, …), nome em kebab-case.
- `src/features/[feature]/SPEC.md` continua sendo o **documento vivo** (estado atual da implementação, conforme `Start.md`). A pasta `specs/NNN-*/` é o **rastro de decisão** do ciclo — não duplicar conteúdo: o SPEC.md vivo referencia `specs/NNN-*/`.
- Templates: `templates/specs/` (ver resolução de overrides em `templates/overrides/README.md`).

---

## 🔁 Fluxo com promoção

```
[1] SPECIFY + CLARIFY → criar spec.md e resolver dúvidas relevantes
        ↓
[2] CLASSIFICAR → todos os limites Lite passam?
        ├── SIM → analisar spec ↔ rules → pedir aprovação humana do spec
        │          → implementar → QA usando spec como contrato
        └── NÃO → promover para Full → plan → tasks → analyze
                   → pedir aprovação humana do sprint-contract
                   → implementar → QA usando sprint-contract
```

### Fase 1 — Specify

- Capturar **o quê** e **por quê** em linguagem simples (histórias de usuário + critérios de aceite).
- **Proibido** citar framework, biblioteca ou banco nesta fase. Se o usuário citar stack, anotar para o plan e manter o spec limpo.
- **Type-First Specs (Obrigatório em TS):** Em projetos com tipagem estática, modelar os tipos e contratos centrais do domínio (ex: assinaturas, estados da UI, tipos union de erros) em um arquivo `specs/NNN-nome/types.ts` ou direto no `spec.md` (como blocos de tipos conceituais) para ancorar logicamente o escopo.
- Marcar pontos vagos com `[PRECISA CLARIFICAR: …]`.

### Fase 2 — Clarify

- Uma pergunta por vez, máximo **5**, tom de colega (mesmo estilo do `kickoff.md`).
- Priorizar os `[PRECISA CLARIFICAR]` de maior impacto (escopo, dados, permissões, estados de erro).
- Registrar cada resposta na seção **Clarificações** do `spec.md` (data + pergunta + resposta).
- Se não houver ambiguidade material, registrar no spec que a conversa já forneceu as decisões necessárias.

### Gate Lite/Full

O projeto nasce com `runtime/context.yaml → governance.profile: lite`. Uma feature permanece Lite somente quando **todos** forem verdadeiros:

1. Um comportamento ou entregável pequeno e claramente definido.
2. No máximo três critérios de aceite.
3. Estimativa de até três arquivos de implementação alterados.
4. Sem nova dependência, integração externa, entidade, rota, tabela, migração ou camada arquitetural.
5. Sem autenticação, autorização, pagamentos, dados sensíveis, operação destrutiva ou risco relevante de perda de dados.
6. Mudança reversível sem migração.
7. O humano aprovou explicitamente o `spec.md`.

Falhou qualquer item → marcar `Profile: Full` e seguir as fases abaixo. Nunca reduzir Full para Lite para evitar documentação.

### Fase 3 — Plan (somente Full)

- Decidir stack respeitando `runtime/stack.yaml` do projeto (não reinventar; padrão `flows/stack-guide.md`).
- Cobrir: arquitetura da feature, modelo de dados, rotas/contratos, riscos, o que **não** será feito.
- Decisões relevantes → espelhar em `runtime/decisions.yaml`.

#### 🏗️ Classificador de proporcionalidade arquitetural (obrigatório)

> Gate de Arquitetura da `catalog/priority-matrix.skill`. Aplicar o **Gate de Solução** somente nos cinco gatilhos definidos: local primeiro; depois um cluster de `solution-sources.yaml`, máximo três candidatos. Registrar escolha e descartes em `runtime/decisions.yaml`.

Antes de detalhar a arquitetura, declarar o nível da feature e registrar o que foi descartado:

```
[ ] S — ajuste pontual em código existente; sem camada nova, sem entidade nova
[ ] M — feature autocontida; 1–2 arquivos de domínio novos; padrão CRUD/service simples
[ ] L — feature com domínio próprio; múltiplas entidades, serviços ou integrações
[ ] XL — subsistema independente; justifica camada nova (ex.: DDD, event-sourcing, hexagonal)
```

**Regra:** declarar o nível no `plan.md` e registrar em `runtime/decisions.yaml` com o campo `arch_level` + o que foi descartado e por quê.

Exemplos de descarte obrigatório:
- Nível S/M → "DDD descartado: ausência de complexidade de domínio"
- Nível M/L → "Event-sourcing descartado: sem requisito de auditoria temporal"
- Nível L → "Hexagonal descartado: integração única, inversão de dependência não justificada"

Teste de saída desta fase: o agente consegue completar a frase *"Esta feature é nível [X] porque [critério]; descartei [padrão] por [razão]"* com dados concretos do spec? Se não, o nível não foi classificado — voltar e classificar.

> **Checklist do Analyze (Fase 5):** adicionar item — `[ ] O padrão arquitetural é proporcional ao nível declarado?`

### Fase 4 — Tasks (somente Full)

- **Padrão "júnior sem contexto":** escrever cada tarefa para um dev júnior competente que **não conhece o projeto nem leu esta conversa**. Toda tarefa tem: path de arquivo exato + o que fazer + **como verificar** (comando/ação + resultado esperado). Teste mental: uma sessão nova de IA executaria a tarefa só com `tasks.md` + `runtime/*.yaml` + SPEC.md? Se não, falta detalhe.
- Ordenar por dependência (modelos → serviços → UI). Tarefas independentes recebem `[P]` (paralelizáveis).
- Agrupar por história de usuário, com **checkpoint** testável ao fim de cada grupo.
- Decisão tomada só no chat não pode ser pré-requisito de tarefa — mover para `plan.md` ou `runtime/decisions.yaml`.

### Fase 5 — Analyze (gate de consistência)

No Lite, checar antes de pedir aprovação do `spec.md`:

```
[ ] Todos os sete limites Lite passam?
[ ] Critérios e riscos estão preenchidos, sem placeholders?
[ ] A solução mínima e o Gate de Solução aplicável foram avaliados?
[ ] rules.yaml e RULES.md continuam respeitados?
```

No Full, checar antes de pedir aprovação do contrato:

```
[ ] Todo critério de aceite do spec.md tem tarefa correspondente em tasks.md?
[ ] Alguma tarefa não rastreia para nenhum requisito? (over-engineering → cortar)
[ ] plan.md contradiz o spec.md em algum ponto?
[ ] Alguma decisão viola runtime/rules.yaml ou RULES.md? (constitution check)
[ ] Restam [PRECISA CLARIFICAR] não resolvidos?
[ ] Os tipos e assinaturas (`types.ts`) estão mapeados, passam no validador do compilador e cobrem todos os caminhos felizes e de exceção?
[ ] O padrão arquitetural é proporcional ao nível declarado (S/M/L/XL)?
[ ] Gate de Solução cumprido quando acionado? (ou marcado não aplicável com motivo)
```

Qualquer item reprovado → corrigir artefatos **antes** de seguir. Reportar resultado em 3–5 linhas em português simples.

### Fase 6 — Aprovação + Implementação

1. Lite: apresentar o `spec.md` e **não implementar antes do "sim"** do usuário; registrar `Status: aprovado` e `Aprovação humana: sim — DATA`.
2. Full: gerar `sprint-contract.md` e **não implementar antes do "sim"** do usuário.
3. Implementar; no Full, marcar `tasks.md`. No Lite, executar diretamente contra os critérios do spec.
4. Rodar `qa-gate.skill`: Lite usa `spec.md` como contrato; Full usa `sprint-contract.md`.
5. Atualizar `runtime/handoff.yaml` + `runtime/active-feature.yaml` e o SPEC vivo quando existir.

---

## ⚖️ Regras

- **Sem código antes da aprovação humana.** O pedido original nunca substitui essa pausa no Lite ou Full.
- Lite contém somente `spec.md`; criar plan/tasks/contrato nele é overprocessing e falha de coerência.
- Full mantém specify → clarify → plan → tasks → analyze → contrato.
- Ajuste trivial **não** passa por este fluxo somente se cumprir os 4 critérios rígidos do HARD-GATE (incluindo declaração explícita no chat) — e mantém QA Gate.
- `rules.yaml` + `RULES.md` funcionam como **constitution**: toda fase pode ser reprovada por violação deles.
- Idioma dos artefatos: segue `runtime/context.yaml` → `language.docs` (default português simples, legível por não-programador; exceto blocos de código). Copy de UI implementada segue `language.product`.

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-08-21
