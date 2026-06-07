# qa-protocol.md — Portaria de qualidade (Fase 1–2)

> **Relatórios:** português simples  
> **Gate rígido:** feature **não** conclui sem `qa.last_status: pass`  
> **Fase 4 Playwright:** **inativa** — rascunhos em `skills/_deferred/phase4-playwright/`

---

## Para quem constrói sozinho

1. **Contrato da sprint** — você aprova  
2. **QA Gate** — agente pode reprovar  
3. **Seu teste** — 5 min no navegador  
4. **Só então** concluído  

---

## Fluxo (v5.1 — ativo hoje)

```txt
Ideia → Especialista que Pergunta → sprint-contract (aprovação)
     → Implementar
     → qa-smoke (build/lint)
     → qa-gate (relatório PASS/FAIL)
     → você testa no browser → handoff pass
```

**Proibido:** concluir feature com QA FAIL.

---

## Dimensões (0–10)

| Dimensão | Peso | Em português |
|----------|------|--------------|
| Funciona | 40% | Abre? Botões respondem? |
| Completo | 25% | Contrato entregue? |
| Estável | 20% | Build/lint ok? |
| Usável | 10% | Próximo passo óbvio? |
| Visual | 5% | Layout ok no mobile? |

**PASS:** Funciona ≥ 7 **e** Estável = PASS.

Relatório: `templates/qa-report.md` → `qa/reports/`

---

## Fase 4 (futuro — não usar agora)

Playwright MCP + cliques automáticos. Ativar quando você pedir. Ver `_deferred/phase4-playwright/README.md`.

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
> Última atualização: 2026-06-07
