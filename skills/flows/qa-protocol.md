# qa-protocol.md — Portaria de qualidade (Fase 1–2)

> **Relatórios:** português simples  
> **Gate rígido:** feature **não** conclui sem `qa.last_status: pass`  
> **Fase 4 Playwright:** **ativa** — CLI, chromium, `pnpm run test:e2e`; geração de spec via `generate_from_contract: true`

---

## Para quem constrói sozinho

1. **Contrato de entrega** — `spec.md` no Lite ou contrato da sprint no Full; você aprova
2. **QA Gate** — agente pode reprovar  
3. **Seu teste** — 5 min no navegador  
4. **Só então** concluído  

---

## Fluxo (v5.5 — Verificador Independente)

```txt
Ideia → Especialista que Pergunta → spec Lite ou contrato Full (aprovação)
     → Implementar
     → QA Gate (delegado para Subagente OU script independent-qa.py)
     → se PASS → você testa no browser (5 min) → handoff pass
```

**Proibido:** concluir feature com QA FAIL.

---

## Dimensões (0–10)

| Dimensão | Peso | Em português |
|----------|------|--------------|
| Funciona | 30% | Abre? Botões respondem? |
| Completo | 20% | Contrato entregue? |
| Estável | 15% | Build/lint/test ok? |
| Usável | 20% | Próximo passo óbvio? Fluxo intuitivo? |
| Visual | 15% | Layout, hierarquia, consistência com DS? |

**PASS:** Funciona ≥ 7 **e** Estável = PASS **e** Usável ≥ 6 **e** Visual ≥ 6.

Relatório: `templates/qa-report.md` → `qa/reports/`

---

## Fase 4 — Playwright (ativo)

CLI, chromium, `pnpm run test:e2e`. Spec gerado do contrato de entrega aprovado: `spec.md` no Lite ou `sprint-contract.md` no Full. Obrigatório para features com UI (`required_for_ui: true`).

---

## Runtime

`qa.yaml` · `handoff.yaml` · `index.yaml`

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-08-21
