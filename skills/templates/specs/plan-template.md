# plan.md — [Nome da Feature]

> **Feature:** NNN-[nome-kebab]
> **Baseado em:** `spec.md` (status: clarificado)
> **Criado em:** YYYY-MM-DD
> **Protocolo:** `skills/governance/feature-flow.md`

---

<!--
⚠️ REGRA DESTE ARQUIVO: descrever o COMO.
Stack deve respeitar runtime/stack.yaml do projeto (padrão: governance/stack-guide.md).
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

## Riscos e decisões

| Decisão | Alternativa descartada | Motivo |
|---------|------------------------|--------|
| | | |

---

## Constitution check

> Conferir contra `runtime/rules.yaml` + `governance/RULES.md` antes de gerar tasks.

- [ ] Nenhuma regra de segurança violada (Host Guard, .env, validação de entrada)
- [ ] Padrões de código e acessibilidade respeitados
- [ ] Sem dependência ou complexidade não justificada pelo spec

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: YYYY-MM-DD
