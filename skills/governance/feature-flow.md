# feature-flow.md — Fluxo Spec-Driven por Feature

> **Papel:** Protocolo obrigatório para adicionar **novas features** a um projeto já iniciado
> **Gatilho:** "Nova feature" · "Adicionar feature" · "Quero uma nova funcionalidade"
> **Não usar para:** projeto novo (use `kickoff.md`) · ajuste trivial (ver critérios rígidos em "HARD-GATE" abaixo)
> **Inspiração:** ciclo specify → clarify → plan → tasks → analyze do [spec-kit (GitHub)](https://github.com/github/spec-kit), adaptado à governança STARTER

---

## 🚧 HARD-GATE — sem código antes de contrato aprovado

**Não escrever código, não criar arquivo de implementação, não fazer scaffold antes da Fase 6 (contrato aprovado pelo usuário). Isso vale para TODA feature, independente de quão simples ela pareça.**

### Anti-pattern nomeado: "isso é simples demais para precisar de spec"

Essa frase (ou variações: "é só um botão", "o usuário está com pressa", "vou só desta vez") é a racionalização mais comum para pular o fluxo — e é exatamente onde suposições não examinadas causam mais retrabalho. Feature "simples" passa pelo fluxo; o spec pode ter 5 linhas, mas existe e é aprovado.

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

O kickoff cobre o **início** do projeto. Este protocolo cobre a **evolução**: toda feature nova passa por um ciclo curto de especificação antes de qualquer código, com rastro em `specs/`.

Regra central herdada do spec-kit: **o spec define o quê (sem tecnologia); o plan define o como (com tecnologia)**.

---

## 📂 Estrutura por feature

Cada feature ganha uma pasta numerada na raiz do projeto:

```
specs/
  001-nome-da-feature/
    spec.md              ← o quê + por quê (sem stack) — com seção Clarificações
    plan.md              ← como: stack, arquitetura, dados, riscos
    tasks.md             ← tarefas ordenadas, dependências, marcadores [P]
    sprint-contract.md   ← contrato aprovado pelo usuário (template existente)
```

- Numeração sequencial com 3 dígitos (`001`, `002`, …), nome em kebab-case.
- `src/features/[feature]/SPEC.md` continua sendo o **documento vivo** (estado atual da implementação, conforme `Start.md`). A pasta `specs/NNN-*/` é o **rastro de decisão** do ciclo — não duplicar conteúdo: o SPEC.md vivo referencia `specs/NNN-*/`.
- Templates: `templates/specs/` (ver resolução de overrides em `templates/overrides/README.md`).

---

## 🔁 Fluxo (6 fases)

```
[1] SPECIFY  → criar specs/NNN-nome/spec.md (o quê, sem tecnologia)
        ↓
[2] CLARIFY  → até 5 perguntas; respostas registradas em "Clarificações" no spec.md
        ↓
[3] PLAN     → plan.md (stack, dados, arquitetura) — só após clarify
        ↓
[4] TASKS    → tasks.md (ordem, dependências, [P] para paralelizáveis, paths de arquivos)
        ↓
[5] ANALYZE  → checagem cruzada spec ↔ plan ↔ tasks ↔ rules.yaml (constitution)
        ↓
[6] CONTRATO + IMPLEMENTAÇÃO → sprint-contract.md aprovado → implementar → qa-gate.skill
```

### Fase 1 — Specify

- Capturar **o quê** e **por quê** em linguagem simples (histórias de usuário + critérios de aceite).
- **Proibido** citar framework, biblioteca ou banco nesta fase. Se o usuário citar stack, anotar para o plan e manter o spec limpo.
- Marcar pontos vagos com `[PRECISA CLARIFICAR: …]`.

### Fase 2 — Clarify (obrigatória antes do plan)

- Uma pergunta por vez, máximo **5**, tom de colega (mesmo estilo do `kickoff.md`).
- Priorizar os `[PRECISA CLARIFICAR]` de maior impacto (escopo, dados, permissões, estados de erro).
- Registrar cada resposta na seção **Clarificações** do `spec.md` (data + pergunta + resposta).
- Pular **somente** se o usuário disser explicitamente que é spike/protótipo descartável — registrar isso no spec.

### Fase 3 — Plan

- Decidir stack respeitando `runtime/stack.yaml` do projeto (não reinventar; padrão `governance/stack-guide.md`).
- Cobrir: arquitetura da feature, modelo de dados, rotas/contratos, riscos, o que **não** será feito.
- Decisões relevantes → espelhar em `runtime/decisions.yaml`.

### Fase 4 — Tasks

- **Padrão "júnior sem contexto":** escrever cada tarefa para um dev júnior competente que **não conhece o projeto nem leu esta conversa**. Toda tarefa tem: path de arquivo exato + o que fazer + **como verificar** (comando/ação + resultado esperado). Teste mental: uma sessão nova de IA executaria a tarefa só com `tasks.md` + `runtime/*.yaml` + SPEC.md? Se não, falta detalhe.
- Ordenar por dependência (modelos → serviços → UI). Tarefas independentes recebem `[P]` (paralelizáveis).
- Agrupar por história de usuário, com **checkpoint** testável ao fim de cada grupo.
- Decisão tomada só no chat não pode ser pré-requisito de tarefa — mover para `plan.md` ou `runtime/decisions.yaml`.

### Fase 5 — Analyze (gate de consistência)

Checagem cética, antes de pedir aprovação do contrato:

```
[ ] Todo critério de aceite do spec.md tem tarefa correspondente em tasks.md?
[ ] Alguma tarefa não rastreia para nenhum requisito? (over-engineering → cortar)
[ ] plan.md contradiz o spec.md em algum ponto?
[ ] Alguma decisão viola runtime/rules.yaml ou RULES.md? (constitution check)
[ ] Restam [PRECISA CLARIFICAR] não resolvidos?
```

Qualquer item reprovado → corrigir artefatos **antes** de seguir. Reportar resultado em 3–5 linhas em português simples.

### Fase 6 — Contrato + Implementação

1. Gerar `sprint-contract.md` na pasta da feature (template `templates/sprint-contract.md`) a partir dos critérios do spec.
2. **Não implementar antes do "sim"** do usuário no contrato.
3. Implementar seguindo `tasks.md`, marcando tarefas concluídas no próprio arquivo.
4. Ao final: `qa-gate.skill` (obrigatório) → atualizar `src/features/[feature]/SPEC.md` vivo + `runtime/handoff.yaml` + `runtime/active-feature.yaml`.

---

## ⚖️ Regras

- **Sem código antes da fase 6.** Specify/clarify/plan/tasks são só documentos. Ver HARD-GATE no topo.
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
> Última atualização: 2026-06-09
