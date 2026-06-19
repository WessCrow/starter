# tasks.md — Plano de Execução (Daemon & Agentes Paralelos)

> **Feature:** 010-autonomia-agente-daemon
> **Projeto:** STARTER
> **Criado em:** 2026-06-19
> **Status:** rascunho
> **Protocolo:** `skills/flows/feature-flow.md`

---

## 🛠️ Checklist de Implementação

- [ ] **T1: Script daemon_watcher.py** `[P]`
  - **Onde:** `skills/scripts/daemon_watcher.py`
  - **O que fazer:** Criar script Python autônomo que monitora e atualiza o status de comandos em `state.yaml` de forma robusta e persistente.
  - **Como verificar:** Rodar o script, adicionar manualmente um comando em `state.yaml` e observar se ele executa e gera o arquivo de log correspondente.

- [ ] **T2: Script run_parallel_agents.py** `[P]`
  - **Onde:** `skills/scripts/run_parallel_agents.py`
  - **O que fazer:** Criar script Python que consome tarefas de `specs/queue.yaml` e as executa concorrentemente contra as APIs de LLMs via HTTP requests puros, aplicando os patches.
  - **Como verificar:** Criar uma fila fictícia e testar a geração automática de um arquivo simples de código.

- [ ] **T3: Atualização do Schema do state.yaml** `[P]`
  - **Onde:** `skills/core/runtime/schema/state.schema.json`
  - **O que fazer:** Atualizar o schema JSON para incluir e validar a estrutura `daemon` (com chaves `commands` contendo listas de comandos com `id`, `cmd`, `status`, `exit_code`, `log_path`).
  - **Como verificar:** Rodar `python3 skills/core/runtime/validate.py` e garantir que passa com sucesso.

- [ ] **T4: Documentação de Operação** `[P]`
  - **Onde:** `AGENTS.md` e `README.md`
  - **O que fazer:** Adicionar seções explicativas sobre a inicialização do Daemon e o uso das ferramentas de autonomia assíncronas.
  - **Como verificar:** Ler a documentação e garantir clareza cognitiva.

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
