# templates/overrides/ — Customização por Projeto

> **Papel:** permitir que um projeto customize templates **sem editar o core do framework**
> **Inspiração:** sistema de overrides/presets do [spec-kit (GitHub)](https://github.com/github/spec-kit)

---

## Resolução (ordem fixa)

Ao usar qualquer template, o agente resolve nesta ordem e usa o **primeiro encontrado**:

```
1. skills/templates/overrides/[mesmo-path]   ← customização do projeto (prioridade)
2. skills/templates/[path]                   ← core STARTER (padrão)
```

Exemplo: se existir `overrides/specs/spec-template.md`, ele vence `specs/spec-template.md`.

---

## Regras

- Override usa o **mesmo path relativo** do template core que substitui.
- **Nunca** editar o template core para necessidade de um projeto específico — criar override.
- Override deve manter as seções obrigatórias do core (o validador de fluxo e o QA Gate dependem delas); pode adicionar seções, terminologia ou idioma próprios.
- Esta pasta começa vazia (apenas este README). Overrides são criados sob demanda, por projeto.

---

## Casos de uso

- Terminologia do domínio (ex: "paciente" em vez de "usuário" num projeto de saúde)
- Seções extras de compliance/regulatório no spec
- Contrato de sprint com critérios fixos da organização

---

## Overrides ativos

| Path do override | Vence o core | Projeto | O que muda |
|------------------|--------------|---------|------------|
| `sprint-contract.md` | `templates/sprint-contract.md` | `pilot-dashboard-pt` | Adiciona seção **"Critérios fixos da org"** (pt-BR, acessibilidade `aria-*`, responsivo 375px, `pnpm build` PASS, erros em português) e marcador de proveniência. Mantém todas as seções obrigatórias do core. |

### Resolver

`resolve-template.sh <path>` implementa a ordem fixa e imprime a origem (`override` ou `core`):

```
$ ./resolve-template.sh sprint-contract.md
ORIGEM: override
PATH:   .../templates/overrides/sprint-contract.md

$ ./resolve-template.sh roadmap-template.md   # sem override
ORIGEM: core
PATH:   .../templates/roadmap-template.md
```

Evidência da execução (B4): `docs/private/reviews/2026-06-22-b4-override-template.md`.

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-09
