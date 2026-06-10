# spec.md — Seção de Depoimentos

> **Feature:** 001-depoimentos
> **Projeto:** NutriLeve
> **Criado em:** 2026-06-09
> **Status:** aprovado
> **Protocolo:** `skills/governance/feature-flow.md`

---

## Por quê

Visitantes da landing precisam de prova social antes de clicar no WhatsApp. Depoimentos reais (mesmo que fictícios para MVP) aumentam confiança e reduzem objeção de "será que funciona?".

---

## Histórias de usuário

| # | Como… | Quero… | Para… | Prioridade |
|---|-------|--------|-------|------------|
| H1 | visitante indeciso | ler depoimentos de clientes | confiar que o método funciona | alta |
| H2 | visitante no celular | ver depoimentos legíveis sem scroll horizontal | decidir sem esforço | alta |

---

## Critérios de aceite (testáveis)

1. Ao rolar a landing, vejo uma seção "O que dizem nossos clientes" com pelo menos 3 depoimentos (nome + texto).
2. Cada depoimento mostra nome e frase curta em português claro.
3. No celular (375px), depoimentos empilham em coluna única sem overflow horizontal.
4. Build compila sem erros após a implementação.

---

## Fora do escopo

- Vídeos de depoimento
- Carrossel animado ou autoplay
- Integração com CMS ou banco de dados

---

## Clarificações

| Data | Pergunta | Resposta |
|------|----------|----------|
| 2026-06-09 | Os depoimentos são reais ou placeholder? | Placeholder realista para MVP — 3 depoimentos estáticos |
| 2026-06-09 | Onde na página? | Entre "Como funciona" e o CTA final |

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
