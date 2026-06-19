# spec.md — Automação e Orquestração Avançada (Daemon & Agentes Paralelos)

> **Feature:** 010-autonomia-agente-daemon
> **Projeto:** STARTER
> **Criado em:** 2026-06-19
> **Status:** rascunho
> **Protocolo:** `skills/flows/feature-flow.md`

---

## Por quê

Atualmente, o fluxo de desenvolvimento assistido por agentes de IA sofre de duas grandes fricções operacionais impostas pelos ambientes das IDEs (Antigravity, Cursor, VSCode, etc.):
1.  **Fricção de Confirmação:** Cada comando proposto pelo agente (`run_command`) dispara popups de segurança que exigem o clique de aprovação manual do usuário.
2.  **Fricção de Concorrência:** O agente de chat principal é monotarefa e não pode abrir ou gerenciar janelas de chat paralelas para executar subtarefas assíncronas de forma autônoma.

Para resolver essas dores, criamos um sistema de automação local composto por um daemon de execução silenciosa de comandos e um executor assíncrono multi-agente que roda inteiramente em background usando a máquina local.

---

## Histórias de usuário

| # | Como… | Quero… | Para… | Prioridade |
|---|-------|--------|-------|------------|
| **H1** | Agente de IA | Delegar comandos de build, teste e validação de forma assíncrona ao disco | Que eles sejam executados na máquina local pelo sistema sem disparar popups de confirmação para o desenvolvedor humano. | Alta |
| **2** | Desenvolvedor Humano | Executar o monitor Daemon uma única vez ao iniciar o projeto | Permitir que o agente trabalhe em segundo plano de forma silenciosa e ininterrupta. | Alta |
| **3** | Agente de IA (Orquestrador) | Criar uma fila de tarefas em formato estruturado no workspace | Distribuir subtarefas de código para instâncias menores de IA rodarem de forma concorrente em background. | Alta |
| **4** | Desenvolvedor Humano | Apenas revisar a homologação final do QA Gate | Focar nas decisões de negócio e design do produto, deixando a micro-implementação de código 100% nas mãos do ecossistema agêntico. | Alta |

---

## Critérios de aceite (testáveis)

1.  **Daemon Watcher:** O script `daemon_watcher.py` monitora o arquivo `state.yaml`, captura novos comandos pendentes na fila, executa-os localmente através de subprocesso, e grava a saída em arquivos de log em `qa/reports/`.
2.  **Paralelismo de Tarefas:** O script `run_parallel_agents.py` consome tarefas de `specs/queue.yaml` e chama a API de inteligência artificial de forma assíncrona para gerar e escrever o código diretamente no disco.
3.  **Resiliência e Fallbacks:** O Daemon watcher impede loops infinitos de comandos e trata interrupções de execução com segurança.
4.  **Handoff de Estado:** O resultado das execuções assíncronas do Daemon e dos agentes paralelos atualiza o `state.yaml` e o `handoff.yaml`.

---

## Fora do escopo

*   Criar uma aplicação desktop ou extensão de VSCode instalável. O sistema é baseado em scripts Python nativos que rodam no terminal.

---

## Clarificações

> Preenchido na fase Clarify (`feature-flow.md` fase 2). Não apagar respostas.

| Data | Pergunta | Resposta |
|------|----------|----------|
| 2026-06-19 | [PRECISA CLARIFICAR: Quais provedores de API serão suportados no roteador de agentes paralelos por padrão?] | OpenAI, Anthropic e Google Gemini, mapeados a partir de chaves de API padrão nas variáveis de ambiente. |
