# runtime-protocol.md — Protocolo v5 Enterprise

> Schema Validation Layer · Hierarchical Load · Anti-drift

---

## Camadas

| Camada | Formato | Validação |
|--------|---------|-----------|
| Runtime IA | YAML + JSON Schema | `validate.py` |
| Humana | Markdown | Sem schema — narrativa |

---

## Ordem oficial (`index.yaml`)

**Hot:** `rules` · `context` · `state`  
**Warm:** `active-feature` (+ `SPEC.md`)  
**Cold:** `stack` · `architecture` · `decisions` · `routes`

---

## Regras enterprise

1. Todo YAML tem schema correspondente em `runtime/schema/`
2. `validate_before_load: true` — agente deve validar após edições
3. `validate_after_write: true` — obrigatório pós-sessão
4. Chaves inválidas = falha de build de contexto
5. Não duplicar dados hot em cold (DRY no runtime)

---

## Drift prevention

| Risco | Mitigação |
|-------|-----------|
| Chave órfã | `additionalProperties: false` |
| Schema divergente | Um schema por arquivo, versionado no repo |
| Runtime corrompido | `validate.py` em CI / pre-commit |
| Token bloat | Lazy cold + hot mínimo |

---

## Compatibilidade IDE

Qualquer agente com leitura de arquivos: seguir `AGENTS.md` + `index.yaml`.  
Sem dependência de memória entre sessões.

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07
