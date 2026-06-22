# spec.md — Figma Gate

> **Feature:** 008-figma-gate
> **Status:** specify ✓ · clarify ✓
> **Criado em:** 2026-06-21
> **Protocolo:** `skills/flows/feature-flow.md`

---

## O quê

Introduzir um gate de confirmação obrigatório sempre que o agente recebe uma referência Figma — antes de gerar qualquer código. O agente declara o que entendeu da referência visual em formato estruturado e aguarda confirmação explícita do mantenedor antes de prosseguir.

---

## Por quê

Três modos de falha identificados empiricamente em Cursor e Antigravity:

1. Agente ignora o Figma e gera UI do zero
2. Agente interpreta proporções, componentes ou tokens incorretamente
3. Agente gera código visualmente correto mas incompatível com a stack do projeto

Nenhum mecanismo atual bloqueia esses modos antes da geração. O retrabalho resultante é o maior desperdício de tempo reportado no uso real do STARTER.

---

## Critérios de aceite

1. Quando Figma está presente, agente sempre para e declara interpretação antes de codar
2. Declaração tem formato fixo com 5 campos obrigatórios
3. Se usuário não confirmar, agente não avança — sem timeout implícito
4. `feature-flow.md` referencia `figma-gate.skill` como etapa condicional
5. `validate-skills.py` detecta ausência da skill e falha com mensagem clara
6. `INDEX.md` lista `figma-gate.skill` em governance

---

## Clarificações

| # | Pergunta | Resposta |
|---|----------|----------|
| 1 | O gate é obrigatório ou opt-in? | Obrigatório sempre que Figma estiver presente — sem exceção |
| 2 | Onde vive a skill? | `skills/governance/figma-gate.skill` + referenciada em `feature-flow.md` |
| 3 | O gate bloqueia tasks `[P]`? | Sim — nenhuma task de UI pode iniciar antes da confirmação |
| 4 | O que conta como "referência Figma"? | URL Figma, screenshot colada, arquivo exportado, ou menção explícita a componente/tela do Figma |
| 5 | Escopo inclui validação de tokens? | Não nesta sprint — só confirmação de interpretação estrutural |

---

## Formato da declaração (contrato de output)

```
## Figma Gate — confirmação obrigatória

Antes de gerar qualquer código, preciso confirmar o que entendi da referência visual.

1. **Componentes identificados:** [lista dos elementos visuais reconhecidos]
2. **Hierarquia:** [estrutura e relação entre componentes]
3. **Tokens inferidos:** [cores, espaçamento, tipografia — valores ou ausência declarada]
4. **Comportamentos detectados:** [hover, estado vazio, responsividade, animações]
5. **Ambiguidades / não identificado:** [o que não consegui ler ou ficou incerto]

→ Confirma para prosseguir?
```

---

## Fora desta sprint

- Validação automática de tokens contra design system do projeto
- Integração com MCP Figma para leitura estruturada de componentes
- Gate para referências visuais que não sejam Figma (screenshots, PDFs)
- Modo silencioso para features sem UI

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: 2026-06-21
