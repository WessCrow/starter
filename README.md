# STARTER

Comece um projeto novo com mais clareza, menos friccao e sem precisar estudar o framework antes.

## A promessa

Voce entra com uma ideia ainda crua.
O agente transforma isso em direcao inicial, estrutura e proximo passo claro.

## Caminho principal

Se voce ignorar todo o resto, faca so isto:

```txt
copie skills/ + AGENTS.md
diga "Começar projeto"
responda
confirme
```

## O que voce ganha logo na primeira sessao

- um inicio guiado, sem precisar decidir tudo sozinho
- uma base organizada para o seu projeto
- clareza sobre o que entra agora e o que fica para depois

## O que e

Um starter para projetos novos orientado por conversa.
Em vez de montar contexto, estrutura e prioridades manualmente, voce responde poucas perguntas e o agente organiza o comeco com voce.

## Para quem e

- Para quem quer sair do zero sem preparar tudo antes.
- Para quem prefere responder perguntas simples antes de gerar estrutura.
- Para quem quer um caminho principal claro, curto e repetivel.

## Para quem nao e

- Para quem quer um template fechado para sair codando sem conversa.
- Para quem ja tem arquitetura, arquivos iniciais e processo proprios.
- Para quem pretende usar este repositorio inteiro como produto final.

## O minimo que importa

1. `skills/` e `AGENTS.md` sao as unicas coisas que voce copia.
2. `Começar projeto` e o comando que inicia o fluxo guiado.
3. O projeto so comeca de verdade depois que voce responde e confirma.

## Escolha seu ponto de partida

Se voce quer utilidade imediata, pense por perfil:

- `landing page`: para pagina de produto, captacao, validacao de ideia ou espera de lancamento.
  Pode dizer: `Começar projeto` e, nas respostas, explicar que quer uma landing page.

- `SaaS dashboard`: para produto com area logada, metricas, tabelas, configuracoes e fluxo de usuario.
  Pode dizer: `Começar projeto` e, nas respostas, explicar que quer um SaaS com dashboard.

- `app interno`: para painel operacional, sistema administrativo, backoffice ou ferramenta de equipe.
  Pode dizer: `Começar projeto` e, nas respostas, explicar que quer um app interno.

- `design system`: para biblioteca de componentes, tokens, documentacao visual e base de interface.
  Pode dizer: `Começar projeto` e, nas respostas, explicar que quer um design system.

- `backend/API`: para servico, painel de integracao, regras de negocio, rotas e infraestrutura de backend.
  Pode dizer: `Começar projeto` e, nas respostas, explicar que quer um backend ou API.

Se ainda nao souber o perfil, tudo bem. Comece igual e descreva o problema que quer resolver.

## Como isso fica na pratica

```txt
voce chega com:
"quero um SaaS simples para organizar pedidos"

o agente conduz:
- faz poucas perguntas
- propoe um caminho inicial
- resume o que entendeu
- espera sua confirmacao

voce sai com:
- base do projeto
- direcao inicial
- proximo passo claro
```

## Compatibilidade e limites

### Funciona melhor em qual ambiente

- Melhor experiencia em `Cursor`, `Claude Code` e `Antigravity`.
- Compativel com `VSCode`, `Windsurf`, `Cline` e `Roo` se respeitarem `AGENTS.md`.
- Funciona melhor quando o agente consegue ler arquivos, seguir instrucoes e conduzir um kickoff por chat.

### Quando usar

- Quando voce vai iniciar um projeto novo do zero.
- Quando voce quer um kickoff guiado em vez de decidir tudo antes.
- Quando voce quer estrutura, contexto e proximos passos claros logo na primeira sessao.

### Quando nao usar

- Quando o projeto ja existe e tem fluxo proprio bem definido.
- Quando voce quer apenas copiar um template fixo e sair codando sem conversa.
- Quando voce nao quer que o agente faca perguntas antes de montar a base.

### O que ainda esta deferred

- `skills/_deferred/`: rascunhos e capacidades fora do fluxo principal.
- Fase 4 de `Playwright`: existe como material adiado, mas nao faz parte do onboarding padrao.
- `qa-playwright` e MCP dessa fase: inativos por padrao.

### O que e experimental ou futuro

- `linked-skills/`: reservado para skills externas, ainda fora da capability ativa.
- `cache/`: reservado para cache remoto futuro, nao faz parte do uso normal hoje.
- Qualquer fluxo remoto fora de `skills/` local deve ser tratado como nao principal ate virar suporte oficial.

## O sistema cuida do resto

Se voce vir nomes como `runtime`, `governance`, `outputs`, `templates`, `YAML` ou `QA gate`, pense neles como infraestrutura interna.
Para comecar, usar e aprovar o kickoff, voce nao precisa dominar nenhum desses termos.

## Como comecar em 60 segundos

1. Crie ou abra a pasta do seu novo projeto.
2. Copie `skills/` para dentro dela.
3. Copie `AGENTS.md` para dentro dela.
4. No chat, diga: `Começar projeto`
5. Responda as perguntas.
6. Quando o agente resumir, confirme.

## Fluxo visual

```txt
VOCE
  ↓
copia 2 coisas
  - skills/
  - AGENTS.md
  ↓
fala 1 comando
  - "Começar projeto"
  ↓
responde perguntas simples
  ↓
confirma
  ↓
AGENTE
  - organiza o inicio
  - limpa o que for interno
  - cria a base do projeto
```

## O que o STARTER nao pede de voce

- decidir stack antes da conversa
- limpar o starter manualmente
- entender jargao interno
- criar contexto, PRD ou runtime antes do seu ok

## Glossario rapido

- `skills/`: pasta com instrucoes que o agente usa.
- `AGENTS.md`: arquivo com o comportamento principal do agente.
- `Começar projeto`: comando para iniciar o onboarding guiado.
- `interno`: coisas do sistema que voce nao precisa estudar para usar.

## Em resumo

Ao dizer `Começar projeto`, o agente limpa o que veio do framework por engano, faz ate 4 perguntas em portugues simples, resume o plano e so cria a base depois da sua confirmacao.

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07
