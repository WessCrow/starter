# plan.md — Seção de Depoimentos

> **Feature:** 001-depoimentos
> **Baseado em:** `spec.md` (status: aprovado)
> **Criado em:** 2026-06-09
> **Protocolo:** `skills/governance/feature-flow.md`

---

## Stack e dependências

- Stack do projeto: React + Vite + pnpm + Tailwind (existente)
- Novas dependências: nenhuma

---

## Modelo de dados

```ts
type Depoimento = {
  nome: string;
  texto: string;
};
```

Array estático em constante no componente (MVP).

---

## Arquitetura da feature

```
src/modules/landing/components/Depoimentos.tsx   ← novo
src/pages/HomePage.tsx                           ← importar seção
```

Segue padrão das seções Beneficios, ComoFunciona.

---

## Rotas e contratos

N/A — componente estático na home.

---

## Riscos e decisões

| Decisão | Alternativa descartada | Motivo |
|---------|------------------------|--------|
| Dados estáticos no componente | CMS / JSON externo | MVP; sem backend |

---

## Constitution check

- [x] Nenhuma regra de segurança violada
- [x] Padrões de código e acessibilidade respeitados (section + article semânticos)
- [x] Sem dependência não justificada

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
