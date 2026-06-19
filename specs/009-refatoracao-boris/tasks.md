# tasks.md — Plano de Execução Paralelizada (Boris Cherny Style)

> **Feature:** 009-refatoracao-boris
> **Projeto:** STARTER
> **Criado em:** 2026-06-19
> **Status:** rascunho
> **Protocolo:** `skills/flows/feature-flow.md`

---

## 🛠️ Trilha A: Infraestrutura de Tipos & Validação (Janela de Contexto 1)

Esta trilha foca nas garantias de tempo de compilação, regras estritas de lint e templates funcionais.

- [ ] **T1: Regras Estritas no rules.yaml** `[P]`
  - **Onde:** `skills/core/runtime/rules.yaml` (linhas 5-8 e novas seções)
  - **O que fazer:** Adicionar regras explícitas bloqueando `any` e `as any` em código TypeScript e ativando `strict: true`. Definir a obrigação de tratamento funcional de exceções (`functional_error_handling`).
  - **Como verificar:** Rodar `python3 skills/core/runtime/validate.py` e garantir que o YAML é válido.

- [ ] **T2: Ajuste no feature-flow.md (Type-First Specs)** `[P]`
  - **Onde:** `skills/flows/feature-flow.md`
  - **O que fazer:** Reescrever as Fases 1 (Specify), 3 (Plan) e 5 (Analyze) para guiar o agente a definir arquivos de assinatura de tipo (`specs/NNN-nome/types.ts`) como parte do escopo técnico antes da codificação.
  - **Como verificar:** Verificar visualmente a coerência do texto e do fluxo.

- [ ] **T3: Refatoração do qa-smoke.skill (Compiler Gates)** `[P]`
  - **Onde:** `skills/catalog/qa-smoke.skill`
  - **O que fazer:** Adicionar o comando `tsc --noEmit` na lista de comandos do Next.js e React + Vite se o compilador TypeScript estiver configurado, fazendo com que qualquer erro de tipagem reprove a validação do pipeline.
  - **Como verificar:** Executar validações de fumaça localmente em projetos de teste para garantir a detecção do gate.

- [ ] **T4: Templates de Erro Funcional** `[P]`
  - **Onde:** Novo arquivo em `skills/templates/specs/result.ts.template`
  - **O que fazer:** Escrever a estrutura genérica de união de tipos `Result<T, E>` / `Either` com exemplos claros de tratamento de exceções sem usar `try/catch` genéricos.
  - **Como verificar:** Testar a validade do código TypeScript gerado.

---

## 🛠️ Trilha B: DX de Ajustes & Automação de Tokens (Janela de Contexto 2)

Esta trilha foca na desburocratização de tarefas diárias e na automação de processos manuais do agente.

- [ ] **T5: Roteamento de Ajustes no action-router.md** `[P]`
  - **Onde:** `skills/flows/action-router.md`
  - **O que fazer:** Implementar as diretrizes para a tag `#ajuste`, detalhando os critérios rígidos para o pulo das fases de especificação escrita e pulo direto para implementação e QA local.
  - **Como verificar:** Revisar se as regras de roteamento não criam brechas de segurança.

- [ ] **T6: Script de Automação de Contagem de Tokens** `[P]`
  - **Onde:** Novo arquivo em `skills/scripts/calculate_tokens.py`
  - **O que fazer:** Criar script Python para varrer os arquivos monitorados listados no handoff, contar os tokens exatos (com fallback aproximado caso a biblioteca `tiktoken` falhe) e gravar na seção `context_metrics` do `handoff.yaml`.
  - **Como verificar:** Executar `python3 skills/scripts/calculate_tokens.py` e inspecionar a escrita correta no `handoff.yaml`.

- [ ] **T7: Integração do cálculo de tokens no Handoff** `[P]`
  - **Onde:** Integrar na skill correspondente ao fluxo de finalização de sessão ou no protocolo de pós-sessão do `AGENTS.md`.
  - **O que fazer:** Garantir que o script de contagem de tokens rode automaticamente antes do fechamento de tarefas ou commits.
  - **Como verificar:** Executar o pipeline de finalização e observar o preenchimento automático das métricas no YAML.

- [ ] **T8: Configuração de Git Hooks (Husky & Lint-Staged)** `[P]`
  - **Onde:** Novo template de configuração em `skills/templates/git/` ou instrução no `AGENTS.md`
  - **O que fazer:** Definir como configurar e propagar githooks para rodar linting e tsc nos arquivos em stage antes de commits.
  - **Como verificar:** Verificar as instruções descritas para garantir que a DX é limpa e não quebra deploys externos.

---

## 🚀 Instruções de Delegação e Context-Scoping

Para rodar este plano em paralelo usando **dois agentes separados (ou janelas de chat distintas)**, siga os roteiros abaixo para cada janela de contexto:

### Roteiro para o Agente da Janela A (Trilha A: Tipos & Validação)
1. **Comando de Entrada:** *"Olá. Atue na Trilha A do plano em `specs/009-refatoracao-boris/plan.md`. Seu foco é estritamente a infraestrutura de tipos, validações no rules.yaml, qa-smoke.skill e templates de erro. Execute as tarefas T1, T2, T3 e T4 descritas em `specs/009-refatoracao-boris/tasks.md`. Evite alterar arquivos fora desse escopo. Atualize a evolução no tasks.md quando terminar."*

### Roteiro para o Agente da Janela B (Trilha B: DX & Automação)
1. **Comando de Entrada:** *"Olá. Atue na Trilha B do plano em `specs/009-refatoracao-boris/plan.md`. Seu foco é a automação de tokens de contexto (script Python), suporte ao sinal #ajuste no action-router.md e githooks locais. Execute as tarefas T5, T6, T7 e T8 descritas em `specs/009-refatoracao-boris/tasks.md`. Evite alterar arquivos fora desse escopo. Atualize a evolução no tasks.md quando terminar."*

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: 2026-06-19
