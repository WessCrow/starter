# plan.md — Plano Técnico de Engenharia (Daemon & Agentes Paralelos)

> **Feature:** 010-autonomia-agente-daemon
> **Projeto:** STARTER
> **Criado em:** 2026-06-19
> **Status:** rascunho
> **Protocolo:** `skills/flows/feature-flow.md`

---

## Proporcionalidade Arquitetural

*   **Nível:** `M` (Feature autocontida no framework; altera 1 arquivo de estado, adiciona 2 scripts utilitários em `skills/scripts/` e documenta as integrações).
*   **Decisões de Descarte:**
    *   *Descarte de SDKs proprietários:* Descartamos o uso de SDKs pesados (`google-generativeai`, `anthropic`) nos scripts locais para evitar quebrar caso o usuário não os possua instalados no ambiente virtual. Faremos chamadas HTTP nativas usando a biblioteca `urllib` do Python (integrada na biblioteca padrão) ou `requests` se disponível.

---

## Arquitetura de Comunicação (Orientada a Arquivos)

Como o agente da IDE está contido em um sandbox de segurança e não pode disparar comandos sem confirmação direta da UI, usamos os arquivos do workspace como **canal de comunicação assíncrona** (IPC - Inter-Process Communication baseado em arquivos).

```
   ┌─────────────────────────┐
   │                         │
   │   Agente de IA (IDE)    │
   │                         │
   └──────┬───────────▲──────┘
          │ Escreve   │ Lê
          │ Estado    │ Logs/Fila
          ▼           │
     ┌────────────────┴┐
     │   state.yaml    │
     │   queue.yaml    │
     └────────────────▲┘
          │ Lê        │ Escreve
          │ Fila/Cmds │ Logs/Status
          ▼           │
   ┌──────────────────┴──────┐
   │                         │
   │   Processo Daemon Local │ (Executado no terminal pelo humano)
   │                         │
   └─────────────────────────┘
```

### 1. Mecanismo de Execução de Comandos (Daemon Watcher)
*   **Arquivo de Controle:** [state.yaml](file:///Users/drt79427/Desktop/Estudos/STARTER/skills/core/runtime/state.yaml)
*   **Fluxo:**
    1. O Agente de IA adiciona uma chave `daemon` no final de `state.yaml` contendo a lista de comandos a rodar.
    2. O `daemon_watcher.py` (em execução contínua no terminal do host) detecta os comandos pendentes.
    3. O Daemon altera o status para `running`, executa o comando via subprocesso e grava a saída em `qa/reports/daemon_[id].log`.
    4. Ao concluir, atualiza o status para `success` ou `failed` e salva o exit code no YAML.
    5. O Agente de IA lê o YAML de volta na IDE e sabe se a tarefa passou ou falhou.

### 2. Mecanismo de Agentes Paralelos (Task Queue)
*   **Arquivo de Controle:** `specs/queue.yaml`
*   **Fluxo:**
    1. O Agente de IA cria um arquivo de fila com tarefas que podem rodar em paralelo.
    2. O script `run_parallel_agents.py` é acionado pelo Daemon ou pelo terminal e lê a fila.
    3. O script cria threads/requisições paralelas para as APIs de IA (Gemini ou Claude) informando o contexto do arquivo e a alteração desejada.
    4. O script aplica as edições de código diretamente nos arquivos de destino de forma concorrente e atualiza a fila com o status final.

---

## Modelos de API Suportados no Script Paralelo

O executor paralelo lerá as chaves de API das variáveis de ambiente:
*   **Google Gemini:** `GEMINI_API_KEY` (usando o modelo `gemini-2.5-flash` ou `gemini-1.5-flash`).
*   **Anthropic Claude:** `ANTHROPIC_API_KEY` (usando o modelo `claude-3-5-sonnet` ou `claude-3-haiku`).
*   **OpenAI:** `OPENAI_API_KEY` (usando `gpt-4o-mini` ou `gpt-4o`).

---

## Riscos & Mitigações

*   **Risco 1 (Loops Infinitos de Comandos):** O agente de IA pode ficar preso gerando comandos que falham continuamente.
    *   *Mitigação:* O Daemon limitará a execução de um mesmo comando a no máximo 3 tentativas falhas.
*   **Risco 2 (Concorrência de Escrita de Arquivos):** Múltiplos agentes paralelos escrevendo no mesmo arquivo podem corrompê-lo.
    *   *Mitigação:* O executor serializará as tarefas que afetam o mesmo arquivo de destino ou bloqueará a escrita concorrente via locks de arquivo simples.

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
