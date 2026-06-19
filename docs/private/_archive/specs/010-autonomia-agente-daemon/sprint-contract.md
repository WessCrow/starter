# Contrato da sprint — Automação e Orquestração Avançada (Daemon & Agentes Paralelos)

> **Data:** 2026-06-19  
> **Feature:** 010-autonomia-agente-daemon  
> **Aprovado por você:** [x] Sim — só implementar após marcar  
> **Local:** `specs/010-autonomia-agente-daemon/sprint-contract.md`

---

## O que o usuário deve conseguir (em português)

1.  **Desenvolvimento Silencioso (Zero Popups):** Executar comandos de validação, build e testes sem que a IDE mostre popups ou solicite cliques manuais de confirmação a todo instante.
2.  **Paralelização Invisível:** Rodar subtarefas de código concorrentemente em segundo plano sem a necessidade de abrir novas janelas de chat na IDE de forma manual.
3.  **Controle Baseado em Arquivos:** Monitorar e auditar todas as execuções de subprocessos do agente através de arquivos de logs e relatórios simples de status no disco.

---

## Critérios testáveis (o QA vai marcar PASS/FAIL)

| # | Critério | PASS/FAIL |
|---|----------|-----------|
| **1** | O script `skills/scripts/daemon_watcher.py` lê comandos pendentes de `state.yaml`, altera seu estado para `running`, executa-os localmente e grava logs de saída em `qa/reports/`. | |
| **2** | O script `skills/scripts/run_parallel_agents.py` é capaz de ler e processar tarefas de `specs/queue.yaml` chamando APIs de LLMs em background e atualizando o status. | |
| **3** | O schema de validação `skills/core/runtime/schema/state.schema.json` é atualizado para validar a seção `daemon` no `state.yaml` sem quebrar o validador `validate.py`. | |
| **4** | As instruções operacionais para o monitoramento e o uso do Daemon local estão devidamente integradas e explicadas no `AGENTS.md`. | |

---

## Fora desta sprint (não implementar agora)

*   Servidor web de monitoramento visual dos agentes (usaremos puramente arquivos e terminal).
*   Geração automática de chaves de API locais (o usuário fornece suas chaves no `.env` ou ambiente).

---

## Stack deste projeto (referência)

- [ ] Next.js + pnpm  
- [ ] React + Vite + pnpm  
- [x] Outro: Core do Framework STARTER (Python + YAML + Bash)

---

## Após implementação

- [ ] `qa-gate.skill` executado  
- [ ] Relatório em `qa/reports/`  
- [ ] `handoff.yaml` → `qa.last_status: pass`  

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
