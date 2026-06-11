# AGENTS.md — Runtime OS v5.2 + QA Gate + Host Guard

Compatível: Antigravity · Cursor · Claude Code · VSCode · Windsurf · Cline · Roo.

---

## 0. Novo projeto — comando único

Se o usuário disser **`Começar projeto`** (ou equivalente):

1. **`bash skills/scripts/clean-framework-artifacts.sh`** — Fase 0 (ver `bootstrap-cleanup.md`)
2. Ler `skills/governance/kickoff.md`
3. **Pergunta 0 (idioma):** português ou inglês? → grava `language` (docs/product) em `runtime/context.yaml`; default pt-BR — *não conta no limite de 4*
4. Fazer até **4 perguntas** em português simples (uma por vez)
5. Resumir + **"Posso começar?"** — **não criar arquivos antes do sim**
6. Após sim → `project-starter.skill` + `project-start.md`

O usuário **não** precisa citar stack. Ver `COMECAR-PROJETO.md` na raiz.

**Bootstrap:** colar `skills/` + `AGENTS.md`. Limpeza do framework é **automática** no passo 1 acima.

---

## 0a. Nova feature — fluxo spec-driven (obrigatório)

Se o usuário pedir **nova feature/funcionalidade** em projeto já iniciado:

1. Ler `skills/governance/feature-flow.md`
2. Criar `specs/NNN-nome/` → **specify** (`spec.md`, sem tecnologia) → **clarify** (≤5 perguntas registradas) → **plan** (`plan.md`) → **tasks** (`tasks.md`, dependências + `[P]`)
3. **Analyze:** checar spec ↔ plan ↔ tasks ↔ `rules.yaml` antes do contrato
4. `sprint-contract.md` aprovado → implementar → QA Gate (seção 3)

Templates: `skills/templates/specs/` (resolução: `templates/overrides/` vence o core — ver `templates/overrides/README.md`).
**HARD-GATE:** sem código antes do contrato aprovado, mesmo em feature "simples". Ajuste trivial só escapa do fluxo cumprindo os 4 critérios rígidos de `feature-flow.md` (≤ ~20 linhas, sem entidade/estado novo, sem comportamento novo visível, **declarado explicitamente no chat**) — e mantém QA. Na dúvida, é feature.

---

## 0b. Alinhamento de Estado Multi-IDE (Sem Quebras de Histórico)

Ao abrir este repositório em uma IDE diferente ou reiniciar uma sessão:
- **Não confie no cache do histórico local da IDE.**
- **Carregue e use estritamente** o arquivo `skills/runtime/state.yaml` e `skills/runtime/handoff.yaml` como a **única fonte da verdade** para restabelecer o contexto, a tarefa ativa e as decisões tomadas.
- Qualquer transição de IDE (ex: migrar do Cursor para o Antigravity) deve ter o estado operacional sincronizado imediatamente a partir dos metadados desses dois arquivos YAML.

---

## 0c. Proteção de Janela (Anti-Alucinação)

Sessão longa (>8 mensagens ou >5 arquivos abertos): sugerir nova janela com resumo via `context-cleaner.skill`.

---

## 0d. Segurança e Isolamento do Host (Host Guard)

Durante a execução de comandos (`run_command`):
- O agente está restrito **estritamente à pasta raiz do workspace** (`/Users/drt79427/Desktop/Estudos/STARTER` ou a raiz do projeto de destino).
- **Proibido:**
  * Executar qualquer comando ou ler/escrever arquivos fora da árvore do projeto (ex: acessar `/tmp`, `/home`, chaves SSH, ou arquivos globais do SO).
  * Executar comandos destrutivos genéricos (como `rm` sem especificar caminhos relativos explicitamente seguros e limitados).
  * Instalar programas globais ou dependências fora do escopo local do projeto.

---

## 0e. Protocolos Comportamentais (sempre ativos)

- **Evidência antes de afirmação:** proibido dizer "pronto", "corrigido" ou "funciona" sem comando executado e saída observada nesta sessão → `skills/local-skills/verify-before-done.skill`. Vale durante toda a sessão, não só no QA Gate.
- **Bug/erro/build FAIL:** causa raiz antes de fix; uma correção por vez; 3 tentativas falhas = parar e reportar → `skills/governance/debugging-protocol.md`.
- **Feedback/crítica do usuário:** verificar antes de implementar; sem concordância performática ("você está certo!" sem checar) → `skills/governance/review-reception.md`.
- **Criar/editar skill ou regra:** ciclo TDD RED→GREEN obrigatório → `skills/governance/skill-testing.md`.

---

## 0f. Hook de Sessão (opt-in — Claude Code)

Para injetar este bootstrap automaticamente em toda sessão (convenção → garantia): registrar `bash skills/scripts/session-start-hook.sh` como hook `SessionStart` no `.claude/settings.json` do projeto (instruções no próprio script). Editores sem suporte a hooks seguem lendo este arquivo normalmente.

---

## 0g. Orquestração por Tier de Modelo (opt-in — economia de modelo)

Complementa §0c/context-scoping: reduz **overhead de modelo** (tier caro em volume), não substitui escopo de contexto. Protocolo: `skills/governance/model-orchestration.md`.

**Papéis:** Orquestrador (chat principal) · Raciocínio profundo (spec, analyze, debug difícil) · Executor rápido (explore, edits mecânicos, shell, tasks `[P]`).

**O usuário não precisa** escolher subagents nem trocar modelo — o agente delega quando aplicável.

| Harness | Comportamento |
|---------|---------------|
| **Cursor / Claude Code** | Delegar via Task/subagent com tier executor quando houver volume ou tasks `[P]` pós-contrato |
| **Antigravity / Windsurf** | Orquestrador no chat; volume via fluxo auxiliar ou nova sessão + `context-cleaner.skill` |
| **Cline / Roo** | Plan/Architect (raciocínio) → Act/Code (executor) — nativo do produto |
| **Demais** | Single-session + `handoff.yaml`; nova janela com resumo se sessão longa (§0c) |

**Nunca delegar (gates):** sprint-contract · QA Gate · verify-before-done · kickoff/spec/clarify/analyze · ajuste trivial.

**Continuidade:** §0b (`state.yaml` + `handoff.yaml`) vale sempre — especialmente ao trocar IDE ou sessão.

---

## 1. Bootstrap

```
skills/runtime/index.yaml
skills/runtime/validate.py   (após editar YAML)
skills/governance/Start-ops.md
```

## 2. Carregamento

| Camada | Arquivos |
|--------|----------|
| Hot | rules, context, state |
| Warm | handoff, qa, active-feature |
| Cold | stack, architecture, decisions, routes |

## 3. QA Gate — obrigatório após implementar

0. Feature do fluxo spec-driven → fase **Analyze** do `feature-flow.md` concluída  
1. Existe `sprint-contract.md` aprovado pelo usuário  
2. Executar `qa-gate.skill` (tom **cético**, relatório **PT-BR simples**)  
3. `qa-smoke.skill` — `pnpm run build` (+ lint/test se scripts existirem; ou `npm` se lock npm)
4. **FAIL** → não marcar feature pronta; listar correções claras  
5. **PASS** → pedir usuário testar 5 min no navegador  

Config: `runtime/qa.yaml` · Protocolo: `governance/qa-protocol.md`

**QA Gate após código:** executar `qa-gate.skill` — sem exceções.

## 4. Stack novos projetos

- **Padrão:** Next.js + pnpm (`governance/stack-guide.md`)  
- Alternativa SPA: React + Vite + pnpm  

## 5. Não carregar como contexto operacional

CONTEXT.md · PRD.md · outputs/*.md (salvo pedido)

## 6. Fase 4 Playwright

**Inativa** — não carregar `qa-playwright` nem MCP. Rascunhos: `skills/_deferred/phase4-playwright/`. Ativar só quando você pedir.

## 7. Pós-sessão

Atualizar handoff + state · `validate.py` 0 failed

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-11
