# Contrato da sprint — Refatoração de Robustez e Automação de DX (Boris Cherny Style)

> **Data:** 2026-06-19  
> **Feature:** 009-refatoracao-boris  
> **Aprovado por você:** [x] Sim — só implementar após marcar  
> **Local:** `specs/009-refatoracao-boris/sprint-contract.md`

---

## O que o usuário deve conseguir (em português)

1. **Garantias Estáticas de Qualidade:** Ter a segurança de que o código gerado pelo agente respeita estritamente o TypeScript (sem atalhos como `any`) e que qualquer erro de compilação ou de linting assíncrono bloqueia automaticamente o pipeline de fumaça.
2. **Automação de DX (Fim das Tarefas Manuais):** Ter as métricas de tokens da janela de contexto calculadas de forma determinística por um script, sem depender da contagem manual e aproximada feita pela IA no handoff.
3. **Pipeline de Edição Veloz (Fast-Track):** Realizar alterações simples de interface ou correções menores marcadas com `#ajuste` sem a necessidade de passar por todo o fluxo documental completo de especificações do STARTER.
4. **Resiliência do Software:** Desenvolver componentes usando tratamento funcional de erros (`Result<T, E>`), garantindo que falhas sejam mapeadas explicitamente no fluxo de estados da UI.

---

## Critérios testáveis (o QA vai marcar PASS/FAIL)

| # | Critério | PASS/FAIL |
|---|----------|-----------|
| **1** | O [feature-flow.md](../../../../../skills/flows/feature-flow.md) inclui a obrigação de modelar os tipos de dados principais antes da codificação da feature. | |
| **2** | O [rules.yaml](../../../../../skills/core/runtime/rules.yaml) bloqueia o uso de `any` e requer o tratamento funcional de erros. | |
| **3** | O [qa-smoke.skill](../../../../../skills/catalog/qa-smoke.skill) executa `tsc --noEmit` como parte obrigatória do build para detectar erros de tipagem. | |
| **4** | Um script Python em `skills/scripts/calculate_tokens.py` calcula dinamicamente o número aproximado de tokens e atualiza o `handoff.yaml` de forma robusta. | |
| **5** | O [action-router.md](../../../../../skills/flows/action-router.md) reconhece a flag `#ajuste` e permite a alteração de código com validação rápida local (Fast-Track). | |
| **6** | Existe um template reutilizável para tratamento funcional de erros (`Result<T, E>`) em `skills/templates/specs/result.ts.template`. | |

---

## Fora desta sprint (não implementar agora)

- Criar uma CLI compilada independente para automação de tokens (será script Python integrado).
- Forçar tratamento funcional em arquivos legados do próprio STARTER. O foco é a infraestrutura de modelagem e validação de novos projetos gerados.

---

## Stack deste projeto (referência)

- [ ] Next.js + pnpm  
- [ ] React + Vite + pnpm  
- [x] Outro: Framework Core do STARTER (Python + YAML + Bash + Markdown)

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
> Última atualização: 2026-06-19
