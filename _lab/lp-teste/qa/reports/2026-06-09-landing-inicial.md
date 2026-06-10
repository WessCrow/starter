# Relatório QA — Landing inicial NutriLeve — 2026-06-09

> **Status final:** PASS (condicionado à checagem de 5 min do usuário no navegador)
> **Idioma:** português simples

## Resumo

Testei a primeira versão da página da NutriLeve. O projeto compila sem erros,
o servidor de preview responde (HTTP 200, título correto) e o código dos CTAs
aponta para o WhatsApp com mensagem pronta e abre em nova aba. A estrutura de
seções segue o contrato. Falta apenas a checagem visual humana no navegador,
exigida pelo protocolo após o PASS.

## Notas por dimensão

| Dimensão | Nota (0–10) | PASS/FAIL | O que foi verificado |
|----------|-------------|-----------|----------------------|
| Funciona | 8 | PASS | preview HTTP 200; links wa.me com target_blank e mensagem codificada |
| Completo | 9 | PASS | 4 critérios do contrato presentes no código e no build |
| Estável | — | PASS | build: `tsc -b && vite build` exit 0; lint: SKIP (script não existe) |
| Usável | 8 | PASS | CTA no primeiro scroll e repetido no fim; fluxo único e óbvio |
| Visual | 7 | PASS | hierarquia clara, paleta verde consistente, grid responsivo md: |

## Contrato da sprint

| # | Critério | Resultado | Detalhe |
|---|----------|-----------|---------|
| 1 | Hero com título, proposta e CTA | PASS | Hero.tsx renderizado no bundle |
| 2 | CTA abre wa.me em nova aba com mensagem | PASS | WhatsAppButton: wa.me + encodeURIComponent + rel noopener |
| 3 | Responsivo 375px | PASS* | classes mobile-first; *confirmar visualmente |
| 4 | Build sem erros | PASS | exit 0, 39 módulos, 147 kB JS |

## Build / terminal

```
✓ 39 modules transformed.
dist/index.html                   0.57 kB
dist/assets/index-D7MyEFmu.css    8.38 kB
dist/assets/index-Oxu3k6_l.js   147.00 kB
✓ built in 1.90s  (exit 0)
```

## Próximo passo

Usuário: abrir o app (`pnpm run dev`) e conferir itens 1–3 do contrato (5 min). Depois dizer "ok".
