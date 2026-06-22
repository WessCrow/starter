<!-- RESOLVED-VIA: skills/templates/overrides/sprint-contract.md -->
<!-- OVERRIDE-SCOPE: pilot-dashboard-pt -->
<!-- Override de projeto. Vence skills/templates/sprint-contract.md (core). Core permanece intacto. -->

# Contrato da sprint — [Nome da feature]

> **Projeto:** pilot-dashboard-pt (Dashboard de Clientes · PT-BR)
> **Resolução:** este template foi carregado de `templates/overrides/` — venceu o core.
> **Data:** YYYY-MM-DD
> **Feature:** [id]
> **Aprovado por você:** [ ] Sim — só implementar após marcar
> **Local:** kickoff → raiz do projeto · feature spec-driven → `specs/NNN-[feature]/sprint-contract.md`
> **Aprovação kickoff:** o "sim" da Fase 2 do `kickoff.md` = aprovação deste contrato (marcar [x] Sim)

---

## O que o usuário deve conseguir (em português)

1. 
2. 
3. 

---

## Critérios testáveis (o QA vai marcar PASS/FAIL)

| # | Critério | PASS/FAIL |
|---|----------|-----------|
| 1 | Ao abrir a tela X, vejo … | |
| 2 | Ao clicar em Y, acontece … | |
| 3 | No celular (375px), … funciona | |
| 4 | Se erro, mensagem clara em português | |

---

## Critérios fixos da org (override — sempre obrigatórios neste projeto)

> Estes critérios são adicionados pelo override e valem para **toda** feature do `pilot-dashboard-pt`,
> além dos critérios específicos da sprint acima. O QA Gate também marca PASS/FAIL aqui.

| # | Critério fixo | PASS/FAIL |
|---|---------------|-----------|
| F1 | UI 100% em **pt-BR** (sem texto solto em inglês na tela) | |
| F2 | **Acessibilidade:** controles interativos expõem `aria-*` correto (`aria-pressed`/`aria-label`) e são navegáveis por teclado | |
| F3 | **Responsivo:** layout sem quebra a 375px (mobile-first) | |
| F4 | `pnpm run build` sem erros de TypeScript | |
| F5 | Mensagens de erro claras e em português | |

---

## Fora desta sprint (não implementar agora)

- 
- 

---

## Stack deste projeto (referência)

- [x] Next.js (App Router) + TypeScript + Tailwind + pnpm
- [ ] React + Vite + pnpm
- [ ] Outro: ___

---

## Após implementação

- [ ] `qa-gate.skill` executado
- [ ] Relatório em `qa/reports/`
- [ ] `handoff.yaml` → `qa.last_status: pass`
- [ ] Você testou no navegador (5 min)

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-22
