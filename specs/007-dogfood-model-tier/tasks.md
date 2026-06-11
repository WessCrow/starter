# Tasks — 007-dogfood-model-tier

| Done | ID | Dep | Arquivo | Ação | Verificação |
|------|-----|-----|---------|------|-------------|
| [x] | T1 | — | `skills/scripts/validate-skills.py` | Adicionar `validate_model_orchestration_log()`: exige `model-orchestration.md` com seções "Log de testes (TDD)", "Racionalizações proibidas", linhas RED/GREEN/REFACTOR; `AGENTS.md` contém `0g` | `python3 skills/scripts/validate-skills.py` PASS |
| [x] | T2 [P] | — | `COMECAR-PROJETO.md` | Nova subseção ~3 linhas "Economia de modelo (opcional)" → §0g + link `model-orchestration.md` | grep `0g` no arquivo |
| [x] | T3 [P] | — | `README.md` | Nova linha na tabela ganhos: orquestração por tier / economia de modelo (§0g) | grep `0g` ou `orquestração` |
| [x] | T4 [P] | — | `skills/INDEX.md` | Linha governance: `model-orchestration.md` | grep `model-orchestration` |

Ordem: T1 pode rodar em paralelo com T2–T4 (independentes).
