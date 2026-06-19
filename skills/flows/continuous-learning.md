# continuous-learning.md — Aprendizado Contínuo (Double-Loop Learning)

> **Papel:** Protocolo obrigatório para evolução autônoma de habilidades e prevenção de erros
> **Gatilho:** Fim de uma sessão de desenvolvimento, fechamento de sprint ou execução do daemon periódico
> **Inspiração:** Arquiteturas de auto-reflexão e alinhamento humano de IA

---

## 🎯 Objetivo

Assegurar que as correções que o desenvolvedor humano faz no código ou nas configurações (`rules.yaml`, `.skill`) após a atuação da IA não se percam. O objetivo é transformar cada ajuste pontual em dados de treinamento que reescrevem as instruções do STARTER para sempre, prevenindo a reincidência de erros.

---

## 🔁 O Fluxo de Feedback Duplo (Double-Loop)

```
+--------------------------------------------------------------+
|                        LOOP 1 (Interno)                      |
|                                                              |
|  [Agent Run] ---> [QA Gate] ---> [record_session.py]         |
|                                        |                     |
|                                        v                     |
|                                 [Trace Log File]             |
+--------------------------------------------------------------+
                                         |
                                         v
+--------------------------------------------------------------+
|                        LOOP 2 (Externo)                      |
|                                                              |
|  [Diffs Humanos]                                             |
|        |                                                     |
|        +-----> [continuous_learner.py] ---> [Proposta Patch] |
+--------------------------------------------------------------+
                                                     |
                                                     v
+--------------------------------------------------------------+
|                     LOOP 3 (Evaluator / Juiz)                |
|                                                              |
|  [validate-skills.py] ---> [Autonomy Dial] ---> [Merged]     |
+--------------------------------------------------------------+
```

---

## 1. Loop 1 (O Loop Interno - Gravação)

A cada execução do agente, todas as ações importantes, saídas de comandos e decisões de arquitetura são salvas. Sem registro, não há aprendizado.

- **Trigger:** Acionado automaticamente no final da sessão pelo script de QA ou gancho de fechamento.
- **Ação:** O script `record_session.py` compila os metadados do `handoff.yaml` e as alterações no git, gerando um log de trace estruturado em `qa/runs/session-[timestamp].jsonl`.
- **Conteúdo do trace:**
  - Identificador da sessão e feature ativa.
  - Comandos executados com seus códigos de saída e trechos de erros.
  - Alterações geradas na base de código.

---

## 2. Loop 2 (O Loop Externo - Aprendizado)

Um agente secundário com foco analítico compila o histórico e descobre onde o agente cometeu falhas ou foi corrigido por um humano.

- **Trigger:** Rodado sob demanda (`python3 skills/infra/scripts/continuous_learner.py`) ou por cron de background.
- **Ação:**
  1. Identifica os arquivos tocados na última sessão que sofreram modificações subsequentes pelo humano (comparando o trace da sessão contra o histórico de commits reais do git).
  2. Extrai a diferença (*human override*) e o motivo conceitual do desvio.
  3. Formula um prompt direcionado utilizando a habilidade `learn.skill` para propor uma modificação estruturada no arquivo `.skill` ou `rules.yaml` correspondente.

---

## 3. O Portão de Regressão (Evaluator / Juiz)

Proibir alterações que resolvam um caso específico mas quebrem outras regras silenciosamente.

- **Validação Estática:** Toda proposta de alteração de skill gerada pelo Loop 2 deve ser submetida a `validate-skills.py` para verificar:
  - Respeito ao orçamento de contexto (`LOCAL_SKILL_FILE_BUDGET`).
  - Integridade de links e snippets obrigatórios.
- **Controle de Autonomia (Autonomy Dial):**
  - **Sugestão (Manual):** O diff da skill é impresso e salvo como proposta para aprovação do usuário.
  - **Híbrido:** O script solicita confirmação (`[y/N]`) no terminal antes de aplicar a mudança.
  - **Total:** O script aplica a mudança diretamente caso todas as validações automáticas deem `PASS`.

---

## ⚖️ Regras de Evolução de Instruções

1. **Reticência a Patches Extensos:** Alterações sugeridas em habilidades devem ser concisas e cirúrgicas. Nunca reescrever uma skill inteira para corrigir um desvio pontual.
2. **Preservação de Rastreabilidade:** Toda alteração de skill feita pelo Loop 2 deve adicionar uma entrada na seção `## Log de testes (TDD)` da respectiva skill contendo:
   - Data da alteração.
   - Cenário falho identificado (RED).
   - Solução adotada (GREEN).
3. **Não diluir o Tom e Voz:** As alterações automáticas devem preservar o tom especialista e conciso e a formatação semântica estabelecida.

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: 2026-06-19
