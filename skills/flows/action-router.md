# action-router.md — Roteador por Tipo de Ação + Gate de Fidelidade

> **Camada base (portável):** lida por qualquer IDE — Antigravity · Cursor · Claude Code · Windsurf · Cline · Roo.
> **Turbo (Claude):** `catalog/action-router.skill`.
> **AGENTS.md §0h** resume; este arquivo é a referência completa.

---

## Por que existe

Resolve dois desperdícios crônicos (Lean):

1. **Overprocessing de governança** — contrato de definição imposto em toda ação, até num ajuste de 3 linhas.
2. **Baixa fidelidade** — UI gerada sem referência (ignora Figma), com tokens mal traduzidos, ou com stack/convenção que não encaixa no projeto.

A regra de ouro: **o contrato só aparece quando agrega valor; a validação de fidelidade é imposta na fonte, não na revisão humana.**

---

## 1. Classificação híbrida (com o usuário no volante)

O agente decide o **modo da ação** combinando inferência + sinal explícito. **O sinal explícito sempre vence.** Nenhuma ação destrutiva sem aval.

### Sinais explícitos (override)

| Flag | Modo | Significado |
|------|------|-------------|
| `#novo` | NOVO | Projeto novo ou definição estrutural |
| `#feature` | FEATURE | Nova funcionalidade em projeto existente |
| `#ajuste` | AJUSTE | Correção/refino de código existente |
| `#figma` | FIGMA | Implementar UI a partir de design Figma |
| `#doc` | DOC | Gerar/atualizar documentação |

### Inferência (default, quando não há flag)

```
[1] Repo vazio / sem runtime/context.yaml ............ → NOVO
[2] Pedido cita entidade/estado/comportamento novo ... → FEATURE
[3] URL Figma presente OU pedido de "implementar UI" . → FIGMA
[4] Edita arquivo existente, escopo ≤ ~20 linhas,
    sem entidade/estado/comportamento novo ............ → AJUSTE
[5] Pedido é só sobre documentação ................... → DOC
[6] Ambíguo .......................................... → perguntar 1x e assumir o mais conservador (FEATURE)
```

> **Regra de desempate:** na dúvida entre AJUSTE e FEATURE, **é FEATURE** (mantém o HARD-GATE do `feature-flow.md`). Inferência nunca rebaixa o nível de governança sem flag explícita do usuário.

---

## 2. Matriz de Ativação de Squads e Roteamento (v5.5)

A governança, os papéis ativos e as etapas obrigatórias de cada ação são obtidas diretamente da `activation_matrix` do `routes.yaml`:

| Modo | Squad Ativo | Etapas / Ações a Executar |
|------|-------------|---------------------------|
| **NOVO** | `[orchestrator, product_strategist, architect]` | kickoff, plan, contract |
| **FEATURE** | `[orchestrator, product_strategist, architect, implementer, independent_qa, doc_writer]` | specify, clarify, plan, tasks, implement, qa_verification, documentation |
| **AJUSTE** | `[implementer, local_qa]` | implement, smoke_check (ajuste leve) |
| **FIGMA** | `[orchestrator, designer, implementer, independent_qa, doc_writer]` | fidelity_gate, implement, qa_verification, documentation |
| **DOC** | `[doc_writer]` | document |

Legenda de papéis: `orchestrator` (mediação), `product_strategist` (clarificação), `architect` (contrato), `implementer` (código), `independent_qa` (validador sético independente), `doc_writer` (especialista de documentação).

**Princípio:** `AJUSTE` e `DOC` **nunca** recriam contrato — só consultam `runtime/*.yaml` + `SPEC.md`. Isso mata o overprocessing.

---

## 3. Gate de Fidelidade Figma (mata os 3 modos de falha)

Disparado em **modo FIGMA** e em qualquer modo que toque UI com design de referência. É um **HARD-GATE**: sem PASS, a UI não é dada como pronta.

### Falha #1 — Ignorar o Figma e criar do zero

```
PRÉ-CHECK obrigatório antes de codar UI:
  - Figma MCP conectado? (testar get_design_context)
      NÃO → PARAR. Avisar o usuário e pedir para habilitar o MCP. NUNCA inventar UI sem referência.
  - URL Figma fornecida e parseável (fileKey + nodeId)?
      NÃO → pedir ao usuário. Não prosseguir "no chute".
  - get_screenshot capturado?
      NÃO → capturar antes da primeira linha de código (fonte de verdade visual).
```

### Falha #2 — Usa Figma mas erra proporção/cor/componente

```
TRADUÇÃO DE TOKENS (proibido hardcode):
  - Buscar equivalentes via search_design_system ANTES de criar.
  - Mapear Figma → projeto: cor, spacing (4/8/16…), text styles, effects.
  - Qualquer valor sem token correspondente → registrar desvio justificado, não hardcodar silenciosamente.
PARIDADE 1:1:
  - Implementar com get_screenshot aberto.
  - Checklist de fidelidade (Passo 6 de figma-implement-design.skill): spacing, tipografia,
    cor/opacidade, radius/border/shadow, estados, responsividade, overflow, z-index.
```

### Falha #3 — Código bonito que não encaixa no projeto

```
ENCAIXE NO PROJETO (governança local imposta na fonte):
  - Ler rules.yaml (hot) + context.yaml/stack.yaml ANTES de codar.
  - Stack do projeto bate com o que vai ser gerado? Não bate → PARAR e alinhar.
  - Convenções (naming, server components, semântica HTML, sem `any`/console.log) aplicadas.
  - DS verificado: componente já existe? → estender, não duplicar.
```

**Saída do gate:** PASS só quando os três checks passam. FAIL → listar correções claras em PT-BR simples; não marcar pronto.

---

## 4. Documentação — só quando pronto

`DOC` é o **único** modo que gera documentação como entregável. Nos demais modos, a documentação é disparada **apenas após o QA Gate dar PASS** (encadeamento: stack/convenções → fidelidade Figma → lint/test → ✅ → doc). Nunca gerar doc a cada passo intermediário.

---

## 5. Encadeamento do gate (ordem fixa)

```
1. Classificar modo (§1)
2. Aplicar contratos do modo (§2)        ← AJUSTE/DOC pulam recriação
3. [se UI/Figma] Gate de Fidelidade (§3) ← pré-check → tokens → paridade → encaixe
4. QA Gate (AGENTS §3 / qa-protocol.md)  ← exceto AJUSTE trivial = smoke leve
5. [só após PASS] Documentação (§4)
6. Persistir state.yaml + handoff.yaml + SPEC.md
```

---

## 6. Nunca / Sempre

**Nunca:** recriar contrato em AJUSTE/DOC · gerar UI sem Figma quando há design de referência · hardcodar token · dar "pronto" sem evidência (§0e) · rebaixar governança por inferência sem flag · gerar doc antes do PASS.

**Sempre:** sinal explícito vence a inferência · pré-check de MCP antes de UI Figma · ler `rules.yaml` + contexto antes de codar · na dúvida AJUSTE↔FEATURE, é FEATURE · usuário aprova antes de qualquer ação destrutiva.

---

## 7. Interop com o framework

- Complementa, não substitui: `feature-flow.md` (spec-driven), `qa-protocol.md` (QA Gate), `figma-implement-design.skill` (workflow Figma→código), `model-orchestration.md` (tiers).
- `AJUSTE` usa exatamente os 4 critérios rígidos de ajuste trivial já definidos em `feature-flow.md`.
- Continuidade multi-IDE (§0b) vale sempre: o modo classificado e o resultado do gate vão para `handoff.yaml`.

---

> **Autoria:** Wesley Alves · [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · Última atualização: 2026-06-16
