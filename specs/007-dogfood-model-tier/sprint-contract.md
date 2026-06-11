# Contrato — 007-dogfood-model-tier

> **Data:** 2026-06-11  
> **Aprovado por você:** [x] Sim — "pode avançar para o dogfood"

## O que deve funcionar

1. `validate-skills.py` falha se log TDD do protocolo estiver incompleto
2. Três docs públicos referenciam §0g / model-orchestration
3. Implementação usa delegação `[P]` (evidência no log TDD)

## Critérios testáveis

| # | Critério | PASS/FAIL |
|---|----------|-----------|
| 1 | `python3 skills/scripts/validate-skills.py` → 0 failed | PASS |
| 2 | `COMECAR-PROJETO.md` menciona §0g | PASS |
| 3 | `README.md` menciona orquestração/tier | PASS |
| 4 | `INDEX.md` lista model-orchestration.md | PASS |

## Fora desta sprint

- package.json / pnpm build (repo sem app)

## Após implementação

- [x] validate-skills + validate.py
- [x] Log dogfood em model-orchestration.md
- [x] handoff.yaml atualizado
