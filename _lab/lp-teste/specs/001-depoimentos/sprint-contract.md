# Contrato da sprint — Seção de Depoimentos

> **Data:** 2026-06-09
> **Feature:** 001-depoimentos
> **Aprovado por você:** [x] Sim (simulado no feature-flow)

## O que o usuário deve conseguir (em português)

1. Rolar a landing e ver depoimentos de clientes antes do CTA final
2. Ler nome e frase de cada depoimento em português claro
3. Ver tudo legível no celular sem scroll horizontal

## Critérios testáveis (o QA vai marcar PASS/FAIL)

| # | Critério | PASS/FAIL |
|---|----------|-----------|
| 1 | Seção "O que dizem nossos clientes" com ≥3 depoimentos visível na home | |
| 2 | Cada card mostra nome + texto curto | |
| 3 | No celular (375px), cards empilham em coluna sem overflow | |
| 4 | Build compila sem erros | |

## Fora desta sprint (não implementar agora)

- Vídeos, carrossel, CMS

## Stack deste projeto (referência)

- [x] React + Vite + pnpm

## Após implementação

- [ ] `qa-gate.skill` executado
- [ ] Relatório em `qa/reports/`
- [ ] `handoff.yaml` → `qa.last_status: pass`
- [ ] Você testou no navegador (5 min)
