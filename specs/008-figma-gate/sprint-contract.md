# Contrato da sprint — Figma Gate

> **Data:** 2026-06-21
> **Feature:** 008-figma-gate
> **Aprovado por você:** [ ] Sim — só implementar após marcar
> **Local:** `specs/008-figma-gate/sprint-contract.md`

---

## O que o usuário deve conseguir (em português)

1. Quando fornecer qualquer referência ao Figma (URL, screenshot, menção a componente), o agente para automaticamente e exibe uma declaração estruturada do que entendeu antes de escrever qualquer linha de código.
2. A declaração tem sempre os mesmos 5 campos: componentes, hierarquia, tokens, comportamentos e ambiguidades.
3. O agente não avança enquanto o usuário não confirmar explicitamente — sem timeout, sem inferência de silêncio como "sim".
4. O framework detecta automaticamente (via `validate-skills.py`) se o gate foi removido ou esquecido em outra sessão.

---

## Critérios testáveis (o QA vai marcar PASS/FAIL)

| # | Critério | PASS/FAIL |
|---|----------|-----------|
| 1 | Ao receber URL Figma + pedido de implementação, agente emite o bloco de declaração com os 5 campos antes de qualquer código | |
| 2 | Declaração contém exatamente: Componentes identificados, Hierarquia, Tokens inferidos, Comportamentos detectados, Ambiguidades | |
| 3 | Sem confirmação explícita do usuário, agente não gera código nem inicia nenhuma task de UI | |
| 4 | `feature-flow.md` contém etapa `[1.5] FIGMA GATE` com referência ao path `skills/governance/figma-gate.skill` | |
| 5 | `python3 skills/infra/scripts/validate-skills.py` falha com mensagem `"ERRO: skills/governance/figma-gate.skill ausente"` quando a skill não existe | |
| 6 | `skills/INDEX.md` contém seção `## Governance` com entrada para `figma-gate.skill` | |

---

## Fora desta sprint (não implementar agora)

- Validação automática de tokens contra design system do projeto
- Integração com MCP Figma para leitura estruturada de componentes
- Gate para referências visuais que não sejam Figma (screenshots avulsas, PDFs)
- Modo silencioso para features sem UI

---

## Stack deste projeto (referência)

- [ ] Next.js + pnpm
- [ ] React + Vite + pnpm
- [x] Outro: Markdown + YAML (skills/flows) · Python 3 (scripts de validação)

---

## Após implementação

- [ ] `qa-gate.skill` executado
- [ ] Relatório em `qa/reports/`
- [ ] `handoff.yaml` → `qa.last_status: pass`
- [ ] TDD Log preenchido em `skills/governance/figma-gate.skill`
- [ ] Você testou o gate com uma URL Figma real ou fictícia (5 min)

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-21
