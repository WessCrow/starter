# kickoff.md — Comando "Começar projeto"

> **Para:** product designer · não precisa saber stack nem termos técnicos  
> **Skill:** `project-starter` · **Não criar arquivos** antes da confirmação (exceto limpeza Fase 0)

---

## Gatilhos

`Começar projeto` · `Comecar projeto` · `Iniciar projeto` · `Novo projeto` · `Start projeto`

---

## Fase 0 — Limpeza automática (SEMPRE primeiro)

> Protocolo: `flows/bootstrap-cleanup.md`

```bash
bash skills/infra/scripts/clean-framework-artifacts.sh
```

Apaga: `CONTEXT.md`, `PRD.md` (raiz), `skills/core/runtime/`, `skills/outputs/`  
Mantém: `skills/` (resto), `AGENTS.md`

**Pular Fase 0** só se usuário disser "continuar projeto existente".  
Após Fase 0: `project-start.md` [1] restaura `skills/core/runtime/` de `templates/runtime/` somente após o "sim".

Uma linha ao usuário: *"Limpei cópias do framework STARTER; agora vamos ao seu app."*

---

## Regra de ouro

O usuário **não** precisa citar Next.js, pnpm, runtime ou skills. O agente **infere** stack e documenta antes de executar.

---

## Fase 1 — Perguntas (máx. 4 + Pergunta 0 de idioma)

Uma pergunta por vez. Tom de colega, não de formulário técnico.

### Pergunta 0 — Idioma (não conta no limite de 4)

> Antes de começar: a comunicação deste projeto será em **português ou inglês**?  
> Vale para textos do site/app e documentação. Se forem diferentes, me diga os dois.

- Grava `language.docs` e `language.product` em `runtime/context.yaml`; default `pt-BR` nos dois.
- Se já indicado na primeira mensagem → inferir, confirmar no resumo, não perguntar de novo.

> **TDD 2026-06-11 GREEN:** resposta mista ("site para mercado americano, docs em português") → `product: en / docs: pt-BR`. PASS.

### Pergunta 1 — O que é?
> Como você chama esse projeto e, em uma ou duas frases, o que ele faz e para quem?

### Pergunta 2 — Primeiro entregável
> O que você quer ver funcionando primeiro?  
> Pode ser: só estrutura + docs · uma landing · uma tela · MVP com 2–3 fluxos.

### Pergunta 3 — Direção visual
> Tem Figma, site de referência ou direção visual clara? (links, paleta, estilo, o que evitar)  
> Se não tiver, diga "não" — eu proponho uma direção inicial.

Se a resposta vier vaga mas com ambição estética: sintetizar brief com `visual-direction-brief` antes do resumo.

### Pergunta 4 — Fora do escopo (opcional)
> Tem algo que **não** deve entrar nesta primeira versão?

Se usuário já respondeu tudo na primeira mensagem → pular perguntas repetidas, ir direto ao resumo.

---

## Fase 2 — Resumo + confirmação

```markdown
## Entendi assim
- **Projeto:** [nome]
- **Resumo:** [1 frase]
- **Idioma:** [ex: site em inglês, documentos em português]
- **Primeiro passo:** [o que existirá ao final desta sessão]
- **Visual:** [referência, proposta ou brief]
- **Fora do escopo agora:** [lista ou "nenhum definido"]

## O que vou configurar
- **Stack:** [ex: Next.js + Tailwind + shadcn + pnpm] — [1 linha de motivo]
- Na raiz: AGENTS.md, CONTEXT.md, PRD.md (sobre SEU app)
- Pasta skills/: governança, runtime, QA
- Código: [pastas conforme P2]

Posso começar a criar? (sim / ajustar: …)
```

**Aguardar "sim".** O "sim" aqui aprova também o `sprint-contract.md` da primeira entrega — não pedir aprovação duplicada.

---

## Fase 2.5 — UX Diamond (obrigatório se UI)

> Skill: `ux-diamond.skill`

Ativar quando P2 indica tela/landing/MVP/feature com UI. Pular se P2 = "só estrutura + docs".  
Executar **após** confirmação do resumo, **antes** de inferir stack.

```
Fase 2 "sim" → ux-diamond → Fase 3 (stack)
```

---

## Fase 3 — Inferência de stack

| Sinais | Stack | Structure skill |
|--------|-------|-----------------|
| App, produto, login, dashboard, várias telas | Next.js + shadcn + pnpm | `nextjs-structure.skill` |
| Landing única, protótipo leve | React + Vite + shadcn + pnpm | `react-vite-structure.skill` |
| Só docs / estrutura | Next.js (prepara app) ou só `skills/` + docs | conforme P2 |
| API / backend explícito | backend skill | `backend-structure.skill` |
| Dúvida | **Next.js** | `nextjs-structure.skill` |

Registrar em `runtime/stack.yaml` e explicar em 1 linha no CONTEXT.md.

---

## Fase 3b — Tipo de projeto → estrutura `work/` proporcional

Inferir o tipo a partir das respostas P1 + P2. Gerar **apenas os módulos necessários**.

| Tipo detectado | Módulos em `work/` |
|----------------|--------------------|
| `research-only` | `work/research/` |
| `design-only` | `work/visual-foundation/` · `work/design/` |
| `dev-only` | `work/technical-context/` · `work/development/` · `work/qa/` |
| `presentation` | `work/research-light/` · `work/narrative/` |
| `full-product` | `work/product-thinking/` · `work/research/` · `work/visual-foundation/` · `work/design/` · `work/development/` · `work/qa/` · `work/handoff/` |

Sinais de inferência:
- "só pesquisa / relatório / análise" → `research-only`
- "landing / visual / Figma / tela" sem código → `design-only`
- "API / backend / CRUD / código" sem design → `dev-only`
- "apresentação / deck / pitch" → `presentation`
- "app / produto / MVP / múltiplos fluxos" → `full-product`
- Dúvida → `full-product` (pode ser podado depois)

Registrar tipo em `runtime/context.yaml` → `project_type`.

---

## Fase 4 — Execução (após "sim")

```
1. flows/project-start.md
2. Copiar templates/runtime/ → skills/core/runtime/
3. Structure skill detectada
4. CONTEXT.md + PRD.md na raiz (do projeto, não do STARTER)
5. context/ — criar pasta e arquivos de memória:
   - context/decisions.md (de templates/context/decisions.md)
     → preencher entrada inicial com direção aprovada no "sim"
   - context/assumptions.md (de templates/context/assumptions.md)
     → preencher premissas óbvias detectadas nas Fases 1-2
6. work/ — criar apenas módulos do tipo detectado (ver Fase 3b)
7. sprint-contract.md na raiz (se P2 pede UI):
   - critérios a partir do resumo Fase 2 + UX Diamond
   - marcar "Aprovado: [x] Sim (kickoff Fase 2)"
8. skills/outputs/ (BRIEF, ROADMAP, ARCHITECTURE)
9. Código inicial só se P2 pedir tela/MVP
10. validate.py → 0 failed
11. Mensagem final: o que foi criado + próximo passo em 1 frase
```

Sem UI em P2 → **não** gerar sprint-contract.  
**Manter na raiz:** `AGENTS.md`, `CONTEXT.md`, `PRD.md` — nunca apagar após kickoff.

---

## Mensagem final (template)

> Projeto **[nome]** iniciado. Abra `CONTEXT.md` para o resumo. `PRD.md` tem o escopo.  
> Próximo passo: **[ex: pedir nova feature ou testar 5 min no navegador]** — é só me pedir.

---

## Anti-padrões

- Pedir stack/framework/pnpm ao usuário no início
- Criar pastas antes do "sim"
- Deixar CONTEXT/PRD do STARTER na raiz durante kickoff
- Apagar AGENTS.md ou CONTEXT/PRD **do app** após kickoff
- Copiar CONTEXT/PRD do STARTER sem substituir pelo do app

---

## Bootstrap do usuário

Colar na pasta nova: **`skills/`** + **`AGENTS.md`** (opcional: `COMECAR-PROJETO.md`).  
**Não** precisa apagar nada — Fase 0 faz isso automaticamente.

---

> **Autoria:** Wesley Alves · [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · Última atualização: 2026-06-11
