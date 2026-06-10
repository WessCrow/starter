# kickoff.md — Comando "Começar projeto"

> **Para:** product designer · não precisa saber stack nem termos técnicos  
> **Gatilho:** uma frase → o agente pergunta → só depois cria tudo

---

## Gatilhos (qualquer um dispara este protocolo)

```
Começar projeto
Comecar projeto
Iniciar projeto
Novo projeto
Start projeto
```

**Skill:** `project-starter` · **Não criar arquivos** antes da fase de confirmação (exceto limpeza Fase 0).

---

## Fase 0 — Limpeza automática (SEMPRE primeiro)

> Protocolo: `governance/bootstrap-cleanup.md`  
> O usuário **não** apaga manualmente.

**Antes da pergunta 1**, executar:

```bash
bash skills/scripts/clean-framework-artifacts.sh
```

Apaga: `CONTEXT.md`, `PRD.md` (raiz), `skills/runtime/`, `skills/outputs/`  
Mantém: `skills/` (resto), `AGENTS.md`

**Pular Fase 0** só se o usuário disser **continuar projeto existente**.

Uma linha para o usuário: *"Limpei cópias do framework STARTER; agora vamos ao seu app."*

---

## Regra de ouro

O usuário **não** precisa citar Next.js, pnpm, runtime ou skills.  
O agente **infere** stack e documenta em linguagem simples antes de executar.

---

## Fase 1 — Só perguntas (máximo 4)

Fazer **uma pergunta por vez**. Tom de colega, não de formulário técnico.

### Pergunta 1 — O que é?

> **Como você chama esse projeto e, em uma ou duas frases, o que ele faz e para quem?**

Exemplo de resposta boa: *"FlowTask — app para freelancers organizarem clientes e prazos."*

---

### Pergunta 2 — Primeiro entregável

> **O que você quer ver funcionando primeiro?**  
> Pode ser bem pequeno: só estrutura e documentação, uma landing, uma tela, ou um MVP com 2–3 fluxos.

Opções para ajudar (não ler como lista obrigatória):

- Só organizar projeto (pastas + docs, sem tela ainda)
- Uma página / landing
- Uma feature (ex: login, dashboard)
- MVP com fluxo principal

---

### Pergunta 3 — Direção visual

> **Tem Figma, site de referência ou uma direção visual clara?**  
> Se tiver, envie links ou diga: paleta base, estilo desejado, tom tipográfico e o que quer evitar.  
> Se não tiver, diga "não" — eu proponho uma direção inicial.

**Se a resposta vier vaga, mas houver ambição estética clara:** sintetizar um brief curto com `visual-direction-brief` antes do resumo da Fase 2.

---

### Pergunta 4 — Fora do escopo (opcional)

> **Tem algo que **não** deve entrar nesta primeira versão?**  
> Se não souber agora, pode dizer "nada por enquanto".

**Se o usuário já respondeu tudo na primeira mensagem** → pular perguntas repetidas e ir direto ao resumo (Fase 2).

---

## Fase 2 — Resumo + confirmação (antes de criar qualquer pasta)

Apresentar em **português simples**:

```markdown
## Entendi assim

- **Projeto:** [nome]
- **Resumo:** [1 frase]
- **Primeiro passo:** [o que vai existir ao final desta sessão]
- **Visual:** [referência, proposta ou brief de direção visual]
- **Fora do escopo agora:** [lista ou "nenhum definido"]

## O que vou configurar (sem você precisar escolher)

- **Tipo de app:** [ex: site/app web]
- **Stack (técnico — só informativo):** [ex: Next.js + Tailwind + shadcn + pnpm]
- **Na raiz do projeto:** AGENTS.md, CONTEXT.md, PRD.md (sobre SEU app)
- **Pasta skills/:** governança, runtime, QA
- **Código:** [pastas iniciais conforme primeiro entregável]

**Recomendo:** [1 frase — ex: Next.js porque é produto completo com rotas e deploy simples]

Posso começar a criar? (sim / ajustar: …)
```

**Aguardar "sim"** (ou ajuste). **Proibido** criar arquivos antes do sim.

> **Equivalência de aprovação:** o **"sim"** nesta fase aprova também o **contrato da primeira entrega** (`sprint-contract.md` na raiz). Não é necessário pedir aprovação duplicada — o contrato é gerado automaticamente na Fase 4 a partir deste resumo.

---

## Fase 2.5 — UX Diamond (obrigatório se UI)

> Skill: `ux-diamond.skill`

**Quando ativar:** resposta da Pergunta 2 indica tela, landing, MVP ou feature com UI.
**Pular:** se P2 = "só organizar projeto (pastas + docs, sem tela)".

Executar UX Diamond **após** confirmação do resumo, **antes** de inferir stack.
O resultado alimenta o sprint-contract com decisões de UX validadas.

```
Fase 2 "sim" → ★ ux-diamond → Fase 3 (stack)
```

---

## Fase 3 — Inferência de stack (agente decide)

| Sinais nas respostas | Stack padrão | Structure skill |
|----------------------|--------------|-----------------|
| App, produto, login, dashboard, várias telas | Next.js + shadcn + pnpm | `nextjs-structure.skill` |
| Landing única, página rápida, protótipo leve | React + Vite + shadcn + pnpm | `react-vite-structure.skill` |
| Só docs / estrutura, sem app ainda | Next.js (prepara app) ou só `skills/` + docs | conforme P2 |
| API / backend explícito | backend skill | `backend-structure.skill` |
| Dúvida | **Next.js** | `nextjs-structure.skill` |

Registrar escolha em `runtime/stack.yaml` e explicar em 1 linha no CONTEXT.md.

Detalhe técnico: `governance/stack-guide.md`

---

## Fase 4 — Execução (após "sim")

Seguir na ordem:

```
1. governance/project-start.md
2. Copiar templates/runtime/ → skills/runtime/
3. Structure skill detectada
4. CONTEXT.md + PRD.md na raiz (do projeto, não do STARTER)
5. sprint-contract.md na raiz (primeira entrega — template templates/sprint-contract.md)
   → preencher critérios a partir do resumo aprovado na Fase 2
   → marcar "Aprovado por você: [x] Sim" (o "sim" da Fase 2 = aprovação do contrato)
6. skills/outputs/ (BRIEF, ROADMAP, ARCHITECTURE)
7. Código inicial só se P2 pedir tela/MVP — senão só estrutura + docs
8. validate.py → 0 failed
9. Mensagem final: o que foi criado + próximo passo em 1 frase
```

### sprint-contract.md no kickoff (primeira entrega)

Gerar **na raiz do projeto** (não em `specs/`) quando P2 pedir tela, landing ou MVP com UI.
Preencher a partir do resumo da Fase 2 + saída do UX Diamond (se aplicável):

- **O que o usuário deve conseguir:** itens do "Primeiro passo" do resumo
- **Critérios testáveis:** 3–4 linhas verificáveis (Hero, CTA, mobile 375px, build)
- **Fora desta sprint:** itens do "Fora do escopo"
- **Aprovado:** `[x] Sim — aprovado no kickoff (Fase 2)`

Sem UI na P2 → **não** gerar sprint-contract (QA Gate de código só entra com entrega visual).

**Manter na raiz:** `AGENTS.md`, `CONTEXT.md`, `PRD.md` — **nunca apagar** após kickoff.

---

## Mensagem final para o usuário (template)

> Projeto **[nome]** iniciado.  
> Abra `CONTEXT.md` para o resumo. `PRD.md` tem o escopo.  
> Próximo passo: **[ex: pedir nova feature ou testar no navegador 5 min]** — é só me pedir.

---

## Bootstrap do usuário

Colar na pasta nova: **`skills/`** + **`AGENTS.md`** (opcional `COMECAR-PROJETO.md`).  
**Não** precisa apagar nada — a **Fase 0** faz isso ao dizer "Começar projeto".

---

## Anti-padrões

- Pedir stack, framework ou pnpm ao usuário no início
- Criar pastas antes do "sim"
- Deixar CONTEXT/PRD do STARTER na raiz durante kickoff (mistura contexto)
- Apagar AGENTS.md ou CONTEXT/PRD **do app** depois que o kickoff criou
- Copiar CONTEXT/PRD do repositório STARTER e **não** substituir pelo do app

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07
