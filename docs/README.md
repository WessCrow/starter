# Documentação STARTER

## Para quem usa o framework → `public/`

Documentos pensados para leitura e compartilhamento:

| Arquivo | Conteúdo |
|---------|----------|
| [`public/O-QUE-E-O-STARTER.md`](public/O-QUE-E-O-STARTER.md) | Visão geral do produto |
| [`public/lp-github.md`](public/lp-github.md) | Texto/copy para README do GitHub |
| [`public/LANDING-PAGE.md`](public/LANDING-PAGE.md) | Brief da landing page |

## Só na sua máquina → `private/`

Relatórios de teste, planos de melhoria, diagnósticos e meta-docs do mantenedor **não vão para o repositório público**.

Coloque arquivos como:

- `relatorio-teste-*.md`
- `plano-acao-*.md` / `plano-melhoria-*.md`
- `diagnostico.md`
- `STARTER-PRD.md`, `STARTER-CONTEXT.md`

Ver política completa: [`skills/governance/repo-hygiene.md`](../skills/governance/repo-hygiene.md)

```bash
python3 skills/scripts/check-repo-hygiene.py
```
