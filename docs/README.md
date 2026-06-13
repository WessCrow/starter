# Documentação STARTER

## Para quem usa o framework → `public/`

Documentos pensados para leitura e compartilhamento externo.

| Arquivo | Conteúdo |
|---------|----------|
| [`public/O-QUE-E-O-STARTER.md`](public/O-QUE-E-O-STARTER.md) | Visão geral do produto |
| [`public/lp-github.md`](public/lp-github.md) | Copy para README do GitHub |
| [`public/LANDING-PAGE.md`](public/LANDING-PAGE.md) | Brief da landing page |

---

## Só na sua máquina → `private/`

Organizado em camadas (inspirado em Clean Architecture): **domínio estável no centro, execução em volta, backlog/arquivo na periferia**.

### `core/` — Contratos permanentes
O que muda menos. Base de decisão para tudo mais.

| Arquivo | Conteúdo |
|---------|----------|
| `STARTER-PRD.md` | Produto, escopo, features principais |
| `STARTER-CONTEXT.md` | Estado atual do runtime, fase, próximos passos |
| `claude.md` | Instruções do agente (comportamento e governança) |
| `README.md` | Guia do mantenedor |

### `delivered/` — Concluído
Sprints encerradas, relatórios finalizados, planos que viraram código.

### `in-progress/` — Em andamento
Sprint ativa e triagem corrente. Ao concluir, mover para `delivered/`.

### `backlog/` — Planejado / Pendente
Melhorias mapeadas, diagnósticos, planos de pilares futuros aguardando priorização.

### `reviews/` — Revisões e auditorias
Reviews de sprint, diagnósticos completos, planos com rastreabilidade.

### `_archive/` — Descartado
Skills rejeitadas e conteúdo obsoleto. Mantido para referência histórica.

---

> Política de higiene: [`skills/flows/repo-hygiene.md`](../skills/flows/repo-hygiene.md)
>
> Verificar: `python3 skills/infra/scripts/check-repo-hygiene.py`
