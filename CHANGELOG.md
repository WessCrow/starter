# Changelog

Todas as mudanças relevantes deste projeto são documentadas aqui.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o versionamento segue [Semantic Versioning](https://semver.org/lang/pt-BR/).
A partir desta versão, este arquivo é mantido automaticamente por
[release-please](https://github.com/googleapis/release-please) a cada merge na `main`.

## [Unreleased]

## [5.4.0] - 2026-06-16

### Adicionado
- **Action Router** (`flows/action-router.md` + `catalog/action-router.skill`): roteamento por tipo de ação (novo/feature/ajuste/figma/doc) com imposição condicional de contrato — corta overprocessing de governança.
- **Gate de Fidelidade Figma**: pré-check de MCP + screenshot antes de codar, mapeamento obrigatório de tokens e verificação de encaixe de stack — ataca os 3 modos de falha (ignorar Figma, tokens errados, stack/convenção errada).
- `AGENTS.md` §0h documentando o Action Router; registro em `Start.md` e `INDEX.md`.

### Alterado
- Higiene + TDD do Sprint B (B2+B3+B5); estrutura de `skills/` reorganizada sob Clean Architecture.
- Host Guard funcional com `validate.py` 0-failed; degradação graciosa por ambiente (handoff + schemas).

## [5.3.0] - 2026-06-13

### Adicionado
- Skills de discovery: `discovery`, `shaping`, `design-critique`, `framing-doc` + upgrade do `ux-audit`.
- Fase 4 Playwright ativada (CLI estável, executor Haiku, webServer automático).
- `context.yaml`/`decisions.yaml` + assumptions + `work/` modular por tipo de projeto.
- Orçamento de contexto por camada em `validate.py` (economia verificável).
- Assimilação Superpowers (P3) com 6 padrões testados.

### Alterado
- Consolidação de governança (sprints 003–007) e documentação (Plano 6); Sprint A do Plano Todos-os-Pilares ≥90%.

### Corrigido
- Host Guard: poda de diretórios (`glob('**')` travava em projetos reais).
- CI: versionar seeds de `skills/outputs/` para `validate-skills` no GitHub Actions.

## [5.2.0] - 2026-06-13

### Adicionado
- QA Gate (`qa-gate.skill`) com build obrigatório + revisão cética antes de marcar entrega como pronta.
- Host Guard: bloqueio de comandos perigosos e proteção contra vazamento de `.env`.
- Orquestração por tier de modelo (`AGENTS.md` §0g + `flows/model-orchestration.md`).
- `session-review.skill` — auto-avaliação ao fim de atividade pesada (desempenho, código, custo, sugestões).
- Pipeline de incubação de skills `TESTAR_` (`flows/skill-intake.md`).
- Pilotos sintéticos de dogfooding em `_lab/` (landing EN + dashboard PT).
- Idioma do projeto no kickoff (Pergunta 0; `context.yaml#language`).
- Validadores antidrift: `validate-skills.py`, `check-repo-hygiene.py`, `check-spec-coherence.py`.
- Recomendação do `rtk` como compressor opcional de output de comandos (`kickoff.md`, `stack-guide.md`).
- Tabela de degradação graciosa por editor/plataforma no README.

### Alterado
- `qa-smoke.skill`: PASS reporta resumo; FAIL grava log com `tee` em `qa/reports/` e reporta as últimas 30 linhas.
- `handoff.yaml`: novo bloco `context_metrics` (arquivos carregados, tokens estimados, método declarado).

[Unreleased]: https://github.com/WessCrow/starter/compare/v5.4.0...HEAD
[5.4.0]: https://github.com/WessCrow/starter/compare/v5.3.0...v5.4.0
[5.3.0]: https://github.com/WessCrow/starter/compare/v5.2.0...v5.3.0
[5.2.0]: https://github.com/WessCrow/starter/releases/tag/v5.2.0
