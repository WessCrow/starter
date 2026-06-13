# Comece em menos de 1 minuto

Voce nao precisa estudar o sistema.
Voce so precisa iniciar a conversa certa.

## O que fazer

1. Cole `skills/` na pasta nova.
2. Cole `AGENTS.md` na pasta nova.
3. Diga `Começar projeto`.
4. Responda as perguntas.
5. Confirme.

## O caminho principal

```txt
skills/ + AGENTS.md
        ↓
 diga "Começar projeto"
        ↓
responder perguntas
        ↓
       sim
```

## O que acontece depois

O agente:

1. limpa sozinho o que veio do starter por engano
2. faz 3-4 perguntas sobre o seu app
3. pede "Posso começar?"
4. cria a base inicial do seu projeto

## O que voce leva da primeira conversa

- direcao inicial
- estrutura de partida
- proximo passo claro

## Exemplo rapido

```txt
voce:
"Começar projeto"

depois:
"quero uma landing para validar uma consultoria"

fim do kickoff:
o agente resume, voce confirma e o projeto comeca
```

## O que voce pode ignorar

Se aparecerem termos como `runtime`, `governance`, `outputs`, `templates`, `YAML` ou `QA gate`, pode ignorar no inicio.
Isso e interno do sistema. Para usar, voce so precisa copiar `skills/` + `AGENTS.md` e dizer `Começar projeto`.

## Economia de modelo (opcional)

Em Cursor e Antigravity, o agente pode delegar automaticamente tarefas pesadas (explore, edits mecânicos, shell) para modelos mais leves e econômicos.
Você não precisa escolher modelo nem subagent — isso é opcional e transparente.
Detalhes em `AGENTS.md` §0g e `skills/flows/model-orchestration.md`.

## Compatibilidade rapida

- Melhor em `Cursor`, `Claude Code` e `Antigravity`.
- Compativel com outros agentes que sigam `AGENTS.md`.
- Feito para `projeto novo`, nao para substituir um processo proprio ja maduro.

## O que ainda nao faz parte do fluxo principal

- `skills/_deferred/`
- Fase 4 de `Playwright`
- `linked-skills/` e `cache/`

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07
