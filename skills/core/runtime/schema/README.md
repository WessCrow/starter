# Runtime Schemas

JSON Schema Draft 2020-12. Validador: `../validate.py` (injeta `v` + `updated` via merge de `_meta`).

## Mapeamento

| Schema | YAML |
|--------|------|
| `index.schema.json` | `index.yaml` |
| `context.schema.json` | `context.yaml` |
| `stack.schema.json` | `stack.yaml` (app **ou** meta runtime) |
| `rules.schema.json` | `rules.yaml` |
| `state.schema.json` | `state.yaml` |
| `active-feature.schema.json` | `active-feature.yaml` |
| `decisions.schema.json` | `decisions.yaml` |
| `routes.schema.json` | `routes.yaml` |
| `architecture.schema.json` | `architecture.yaml` |

## stack.schema.json — oneOf

1. **AppStack** — `frontend` obrigatório (+ `bundler`, `ui`, `architecture`)
2. **MetaRuntimeStack** — `type` obrigatório (STARTER governance)

## Extensão

1. Editar schema  
2. Editar YAML  
3. `python3 skills/core/runtime/validate.py`  
4. Registrar em `index.yaml` → `schemas` se novo arquivo

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07
