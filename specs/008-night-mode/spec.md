# spec.md — Night Mode / Autonomous Safe Mode

> **Feature:** 008-night-mode
> **Projeto:** STARTER
> **Criado em:** 2026-06-19
> **Status:** rascunho
> **Protocolo:** `skills/flows/feature-flow.md`

---

<!--
⚠️ REGRA DESTE ARQUIVO: descrever O QUÊ e POR QUÊ.
❌ Proibido citar framework, biblioteca, banco ou stack — isso vai no plan.md.
✅ Pontos vagos: marcar [PRECISA CLARIFICAR: pergunta] e resolver na fase Clarify.
-->

## Por quê

Garantir que o desenvolvedor possa deixar tarefas rodando de forma assíncrona (como à noite ou durante períodos de ausência) com máxima segurança, sabendo que a IA operará em um ambiente controlado, com restrições rígidas contra ações destrutivas (deleções, merges automáticos) e gerando um relatório claro e estruturado ao final.

---

## Histórias de usuário

| # | Como… | Quero… | Para… | Prioridade |
|---|-------|--------|-------|------------|
| H1 | Desenvolvedor/Mantenedor | Ativar um modo seguro e com restrições rígidas (Night Mode) | Delegar tarefas longas (mapeamento, auditoria, testes, pequenas correções) sem medo de quebras ou merges acidentais | alta |
| H2 | Agente de IA | Identificar as diretrizes, restrições e limites ativos no Night Mode | Operar com autonomia calibrada, sabendo exatamente quando parar ou pedir intervenção humana | alta |
| H3 | Desenvolvedor/Mantenedor | Receber um relatório estruturado de handoff e checkpoints ao final da execução | Revisar e aprovar rapidamente o trabalho realizado sem precisar inspecionar manualmente todo o histórico de logs | média |

---

## Critérios de aceite (testáveis)

1. Ao ativar o Night Mode, o agente lê e respeita as regras de restrição de ações (ex: proibido merge automático na branch principal, proibido deploy, proibido deletar arquivos base).
2. Se o agente encontrar uma quebra de testes ou build persistente (mais de 1 tentativa de correção), ele deve pausar o ciclo e salvar o estado atual.
3. Se o agente encontrar uma ambiguidade crítica de arquitetura ou requisito de negócio, ele deve registrar a dúvida na seção de Clarificações e parar a execução, sem tomar decisões arbitrárias.
4. Ao final da execução (seja por conclusão de tarefas, interrupção por erro ou ambiguidade), o agente gera um relatório estruturado contendo: o que foi feito, arquivos alterados, erros encontrados, status dos testes e próximos passos.

---

## Fora do escopo

- Bloqueio físico ou criptográfico de infraestrutura externa (ex: tokens de nuvem/GitHub) que não dependam da instrução do agente ou de scripts locais (guards).
- Execução contínua de tarefas que necessitem de aprovação prévia obrigatória (como deploys reais de produção).

---

## Clarificações

> Preenchido na fase Clarify (`feature-flow.md` fase 2). Não apagar respostas.

| Data | Pergunta | Resposta |
|------|----------|----------|
| 2026-06-19 | [PRECISA CLARIFICAR: Onde devem residir os arquivos de diretrizes e templates do Night Mode? Sob uma pasta `.starter/` na raiz do projeto consumidor, ou integrados à pasta `skills/` e `runtime/` do framework?] | |
| 2026-06-19 | [PRECISA CLARIFICAR: Como as restrições contra ações destrutivas (guards) devem ser garantidas? Apenas com instruções de contexto/prompts ou com hooks e scripts locais rígidos (ex: estendendo o `host-guard.sh` ou criando novos hooks de pre-commit)?] | |
| 2026-06-19 | [PRECISA CLARIFICAR: Qual deve ser o gatilho oficial para o agente entrar em Night Mode? Um comando explícito no chat, um arquivo de estado (`runtime/state.yaml`), ou um argumento na inicialização?] | |

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: 2026-06-19
