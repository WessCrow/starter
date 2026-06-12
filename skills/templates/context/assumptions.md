# assumptions.md — Premissas do Projeto

> **Diferença de decisions.md:** premissa é o que foi assumido sem validação.
> Decisão é escolha ativa. Premissa é risco latente.

---

## Para que serve

Separar o que foi decidido (escolha consciente) do que foi assumido (hipótese não validada).
Evita que o agente trate premissas como fatos em sessões futuras.

---

## Regras do agente

- Preencher no kickoff com as premissas óbvias da Fase 2
- Atualizar quando uma premissa for validada (→ mover para decisions.md) ou invalidada (→ registrar o impacto)
- Manter a lista curta — máximo 10 premissas ativas
- Premissas validadas ficam marcadas com ✓ e data

---

## Template de entrada

```
- [ ] [premissa] — risco: [baixo/médio/alto] — validar com: [como validar]
- [✓ AAAA-MM-DD] [premissa] — validada por: [evidência]
```

---

## Premissas ativas

- [ ] [ex: usuário tem acesso a Figma] — risco: baixo — validar com: pergunta direta
- [ ] [ex: projeto será em Next.js] — risco: médio — validar com: confirmação na Fase 1
- [ ] [ex: deploy no Vercel] — risco: baixo — validar com: primeira entrega

---

## Premissas validadas

<!-- Mover aqui quando confirmadas -->

---

## Premissas invalidadas

<!-- Registrar o impacto quando uma premissa cair -->

