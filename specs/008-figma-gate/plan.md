# plan.md — Figma Gate

> **Feature:** 008-figma-gate
> **Baseado em:** `spec.md` (status: clarify ✓)
> **Criado em:** 2026-06-21
> **Protocolo:** `skills/flows/feature-flow.md`

---

## Stack e dependências

- Stack do projeto: Markdown + YAML para skills e flows; Python 3 para script de validação.
- Novas dependências: Nenhuma. Reusa estrutura de skills existente (`skills/catalog/`, `skills/flows/`) e o validador Python em `skills/infra/scripts/validate-skills.py`.

---

## Nível arquitetural

- **Nível:** [x] S  [ ] M  [ ] L  [ ] XL
- **Justificativa:** Nenhuma entidade, rota ou estado novo. São 4 modificações de arquivo + 1 arquivo novo de skill, todos dentro da árvore `skills/`. Zero impacto em código de produto.
- **Descartados:**
  - M (feature autocontida com domínio novo): descartado — não há domínio; é pura governança de processo.
  - Event-sourcing / DDD: sem pertinência.

---

## Arquivos novos

| Arquivo | Papel |
|---------|-------|
| `skills/governance/figma-gate.skill` | Skill principal: define o gate, o formato da declaração, gatilhos e regra de bloqueio |

---

## Arquivos modificados

| Arquivo | Mudança |
|---------|---------|
| `skills/flows/feature-flow.md` | Adicionar etapa condicional "Figma Gate" entre Fase 1 (Specify) e Fase 3 (Plan) — ativa quando há referência Figma |
| `skills/infra/scripts/validate-skills.py` | Adicionar check: `skills/governance/figma-gate.skill` deve existir; falha com mensagem descritiva se ausente |
| `skills/INDEX.md` | Adicionar seção `## Governance` listando `figma-gate.skill` |

---

## Arquitetura da skill

`figma-gate.skill` deve conter:

1. **Frontmatter YAML** — `name`, `description`, `triggers` (lista de padrões que ativam o gate)
2. **Gatilhos** — o que conta como referência Figma (URL, screenshot, arquivo exportado, menção explícita)
3. **Regra de bloqueio** — nenhuma task `[P]` de UI pode ser iniciada sem confirmação
4. **Formato de declaração** — os 5 campos obrigatórios conforme spec
5. **Protocolo de confirmação** — agente aguarda resposta explícita; sem timeout; sem inferência de silêncio como "sim"
6. **Log TDD** — seção `## TDD Log` com ciclo RED→GREEN documentado após primeiro teste real

---

## Posição no fluxo (feature-flow.md)

```
[1] SPECIFY
        ↓
[1.5] FIGMA GATE (condicional — ativo se Figma presente)
        ↓
[2] CLARIFY
        ↓
[3] PLAN  ...
```

O gate é inserido como sub-etapa nomeada entre Specify e Clarify, com nota: "Se a feature tem referência Figma, executar `figma-gate.skill` antes de qualquer pergunta de clarificação relacionada à UI."

---

## Riscos e decisões

| Decisão | Rastreia para (critério do spec) | Alternativa descartada | Motivo |
|---------|----------------------------------|------------------------|--------|
| Skill em `skills/governance/` (diretório novo) | Critério 2 | `skills/catalog/` | Separar governance de skills de execução — deixa intenção explícita |
| Gate posicionado antes de Clarify | Critério 1, 3 | Após Clarify | Clarificações de UI dependem de interpretação do Figma; gate deve vir antes para não contaminar as perguntas |
| validate-skills.py como guardião | Critério 5 | Checar via README | Script já existente; adicionar um check é zero overhead e dá feedback automático |

---

## Constitution check

- [x] Sem dependência externa nova
- [x] Sem código de produto alterado
- [x] Padrão proporcional ao nível S declarado
- [x] Idioma dos artefatos: português (conforme `runtime/context.yaml`)

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: 2026-06-21
