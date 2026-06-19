# Contrato da sprint — Aprendizado Contínuo (Double-Loop Learning)

> **Data:** 2026-06-19  
> **Feature:** 012-continuous-learning  
> **Aprovado por você:** [x] Sim — só implementar após marcar  
> **Local:** `specs/012-continuous-learning/sprint-contract.md`

---

## O que o usuário deve conseguir (em português)

1. Registrar automaticamente todas as ações de cada sessão do agente em traces locais para auditoria e aprendizado.
2. Identificar discrepâncias entre o que o agente realizou e as correções que o desenvolvedor humano aplicou subsequentemente.
3. Obter propostas estruturadas de melhoria para os arquivos de habilidades (`.skill`) com base nos desalinhamentos encontrados.
4. Ter a garantia de que as habilidades autônomas geradas não regridem nem ferem as regras de governança e orçamentos do framework STARTER.

---

## Critérios testáveis (o QA vai marcar PASS/FAIL)

| # | Critério | PASS/FAIL |
|---|----------|-----------|
| 1 | Um arquivo JSONL é gerado na pasta `qa/runs/` contendo informações estruturadas da sessão do agente após a execução do script. | |
| 2 | O script de aprendizado contínuo detecta divergências operacionais (por exemplo, commits posteriores do desenvolvedor humano em arquivos alterados pelo agente). | |
| 3 | O sistema gera uma proposta de patch fundamentada para as skills baseado na divergência detectada. | |
| 4 | O script de validação de regras (`validate-skills.py`) roda com sucesso incluindo as novas diretivas de aprendizado contínuo. | |

---

## Fora desta sprint (não implementar agora)

- Envio de alertas de divergências para o Slack ou criação automática de Pull Requests no GitHub.
- Interface visual (frontend web) para configuração do Autonomy Dial.

---

## Stack deste projeto (referência)

- [ ] Next.js + pnpm  
- [ ] React + Vite + pnpm  
- [x] Outro: Scripts CLI em Python 3

---

## Após implementação

- [ ] `qa-gate.skill` executado  
- [ ] Relatório em `qa/reports/`  
- [ ] `handoff.yaml` → `qa.last_status: pass`  
- [ ] Você testou no navegador ou terminal (5 min)

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-19
