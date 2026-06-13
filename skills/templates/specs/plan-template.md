# plan.md — [Nome da Feature]

> **Feature:** NNN-[nome-kebab]
> **Baseado em:** `spec.md` (status: clarificado)
> **Criado em:** YYYY-MM-DD
> **Protocolo:** `skills/flows/feature-flow.md`

---

<!--
⚠️ REGRA DESTE ARQUIVO: descrever o COMO.
Stack deve respeitar runtime/stack.yaml do projeto (padrão: flows/stack-guide.md).
Decisões relevantes → espelhar em runtime/decisions.yaml.
-->

## Stack e dependências

- Stack do projeto: [Next.js + pnpm | React + Vite + pnpm | outro]
- Novas dependências (justificar cada uma): 

---

## Modelo de dados

```ts
// Entidades que esta feature cria ou altera
```

---

## Arquitetura da feature

> Pastas/arquivos novos ou alterados, seguindo `skills/structure/`.

```
src/features/[feature]/
  ├── …
```

---

## Rotas e contratos

| Rota/Endpoint | Método | Entrada | Saída |
|---------------|--------|---------|-------|
| | | | |

---

## Nível arquitetural

> Declarar o nível antes de detalhar a arquitetura (ver `flows/feature-flow.md` Fase 3).

- **Nível:** [ ] S  [ ] M  [ ] L  [ ] XL
- **Justificativa:** [por que este nível e não o acima]
- **Descartado:** [padrão descartado] — [motivo]

---

## Riscos e decisões

| Decisão | Rastreia para (critério do spec.md) | Alternativa descartada | Motivo |
|---------|--------------------------------------|------------------------|--------|
| | | | |

---

## Constitution check

> Conferir contra `runtime/rules.yaml` + `flows/RULES.md` antes de gerar tasks.

- [ ] Nenhuma regra de segurança violada (Host Guard, .env, validação de entrada)
- [ ] Padrões de código e acessibilidade respeitados
- [ ] Sem dependência ou complexidade não justificada pelo spec

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: YYYY-MM-DD
