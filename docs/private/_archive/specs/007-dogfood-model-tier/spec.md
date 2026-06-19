# Spec — Dogfood orquestração por tier

> **Feature:** 007-dogfood-model-tier  
> **Status:** specify ✓

## O quê

Validar empiricamente a orquestração por tier (§0g) entregando rastreabilidade mecânica + docs mínimos para usuários Cursor/Antigravity — sem UI.

## Por quê

TDD simulado provou obediência; falta evidência de delegação real com tasks `[P]` pós-contrato.

## Clarificações

| # | Pergunta | Resposta |
|---|----------|----------|
| 1 | Escopo inclui app? | Não — só framework STARTER |
| 2 | Quem aprova contrato? | Mantenedor ("pode avançar para o dogfood") |

## Critérios de aceite (usuário)

1. Validador antidrift exige log TDD em `model-orchestration.md`
2. `COMECAR-PROJETO.md`, `README.md` e `INDEX.md` mencionam §0g
3. Evidência de delegação `[P]` registrada no log TDD do protocolo
