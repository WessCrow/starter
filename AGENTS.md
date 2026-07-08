# AGENTS.md — Runtime OS v5.2 + QA Gate + Host Guard + Action Router

Compatível: Antigravity · Cursor · Claude Code · VSCode · Windsurf · Cline · Roo.

---

## 0. Novo projeto — comando único

Se o usuário disser **`Começar projeto`** (ou equivalente):

1. **`bash skills/infra/scripts/clean-framework-artifacts.sh`** — Fase 0 (ver `bootstrap-cleanup.md`)
2. Ler `skills/flows/kickoff.md`
3. **Pergunta 0 (idioma):** português ou inglês? → grava `language` (docs/product) em `runtime/context.yaml`; default pt-BR — *não conta no limite de 4*
4. Fazer até **4 perguntas** em português simples (uma por vez)
5. Resumir + **"Posso começar?"** — **não criar arquivos antes do sim**
6. Após sim → `project-starter.skill` + `project-start.md`

O usuário **não** precisa citar stack. Ver `COMECAR-PROJETO.md` na raiz.

**Bootstrap:** colar `skills/` + `AGENTS.md`. Limpeza do framework é **automática** no passo 1 acima.

---

## 0a. Nova feature — fluxo spec-driven (obrigatório)

Se o usuário pedir **nova feature/funcionalidade** em projeto já iniciado:

1. Ler `skills/flows/feature-flow.md`
2. Criar `specs/NNN-nome/` → **specify** (`spec.md` sem tecnologia; obrigatório conter seções de *Critérios de Aceite* e *Análise de Riscos*, ambas preenchidas de forma real e sem placeholders) → **clarify** (≤5 perguntas registradas) → **plan** (`plan.md`) → **tasks** (`tasks.md`, dependências + `[P]`)
3. **Analyze:** checar spec ↔ plan ↔ tasks ↔ `rules.yaml` antes do contrato (o validador automático do QA Gate rejeita seções ausentes ou placeholders)
4. `sprint-contract.md` aprovado → implementar → QA Gate (seção 3)

Templates: `skills/templates/specs/` (resolução: `templates/overrides/` vence o core — ver `templates/overrides/README.md`).
**HARD-GATE:** sem código antes do contrato aprovado, mesmo em feature "simples". Ajuste trivial só escapa do fluxo cumprindo os 4 critérios rígidos de `feature-flow.md` (≤ ~20 linhas, sem entidade/estado novo, sem comportamento novo visível, **declarado explicitamente no chat**) — e mantém QA. Na dúvida, é feature.

---

## 0b. Alinhamento de Estado Multi-IDE (Sem Quebras de Histórico)

Ao abrir este repositório em uma IDE diferente ou reiniciar uma sessão:
- **Não confie no cache do histórico local da IDE.**
- **Carregue e use estritamente** o arquivo `skills/core/runtime/state.yaml` e `skills/core/runtime/handoff.yaml` como a **única fonte da verdade** para restabelecer o contexto, a tarefa ativa e as decisões tomadas.
- Qualquer transição de IDE (ex: migrar do Cursor para o Antigravity) deve ter o estado operacional sincronizado imediatamente a partir dos metadados desses dois arquivos YAML.

---

## 0c. Proteção de Janela (Anti-Alucinação)

Sessão longa (>8 mensagens ou >5 arquivos abertos): sugerir nova janela com resumo via `context-cleaner.skill`.

---

## 0d. Segurança e Isolamento do Host (Host Guard)

Modelo em duas camadas — protocolo completo em `skills/flows/host-guard.md`.

**Camada 1 (convenção):** Durante a execução de comandos (`run_command`), o agente está restrito **estritamente à pasta raiz do workspace**.
- **Proibido:** comandos/arquivos fora da árvore do projeto (`/tmp`, `/home`, `~/.ssh`, globais do SO); destrutivos genéricos (`rm -rf` em raiz/home, `mkfs`, `dd` em `/dev/`); pipe-to-shell (`curl … | sh`); instalação global (`npm/pnpm/yarn -g`, `sudo apt|brew`); force push em `main`/`master`.

**Camada 2 (enforce):** Hook `PreToolUse:Bash` executa `skills/infra/scripts/host-guard.sh`, que intercepta cada comando e **bloqueia com exit 2** os padrões acima — determinístico, independente do modelo. Ativação opt-in em `.claude/settings.json` (ver `skills/flows/host-guard.md`).

---

## 0e. Protocolos Comportamentais (sempre ativos)

- **Evidência antes de afirmação:** proibido dizer "pronto", "corrigido" ou "funciona" sem comando executado e saída observada nesta sessão → `skills/catalog/verify-before-done.skill`. Vale durante toda a sessão, não só no QA Gate.
- **Bug/erro/build FAIL:** causa raiz antes de fix; uma correção por vez; 3 tentativas falhas = parar e reportar → `skills/flows/debugging-protocol.md`.
- **Loop de ferramenta/subagente:** freio automático por orçamento (máx 3 iterações ou ~2 min sem progresso na mesma chamada) → parar sozinho, trocar de abordagem ou reportar curto; o usuário nunca precisa cancelar na mão → `skills/flows/loop-breaker.md`.
- **Feedback/crítica do usuário:** verificar antes de implementar; sem concordância performática ("você está certo!" sem checar) → `skills/flows/review-reception.md`.
- **Criar/editar skill ou regra:** ciclo TDD RED→GREEN obrigatório → `skills/flows/skill-testing.md`.

---

## 0f. Hook de Sessão (opt-in — Claude Code)

Para injetar este bootstrap automaticamente em toda sessão (convenção → garantia): registrar `bash skills/infra/scripts/session-start-hook.sh` como hook `SessionStart` no `.claude/settings.json` do projeto (instruções no próprio script). Editores sem suporte a hooks seguem lendo este arquivo normalmente.

---

## 0g. Orquestração por Tier de Modelo (opt-in — economia de modelo)

Complementa §0c/context-scoping: reduz **overhead de modelo** (tier caro em volume), não substitui escopo de contexto. Protocolo: `skills/flows/model-orchestration.md`.

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

## 0h. Roteamento por Tipo de Ação (Action Router)

Decide **o que impor e quando** — corta o overprocessing de governança e impõe fidelidade na fonte. Protocolo completo: `skills/flows/action-router.md`. Turbo (Claude): `catalog/action-router.skill`.

**Híbrido com o usuário no volante:** o agente infere o modo pelo estado do repo; **o sinal explícito sempre sobrepõe**; nada destrutivo sem aval.

| Sinal | Modo | Governança imposta |
|-------|------|--------------------|
| `#novo` | NOVO | kickoff §0 + `priority-matrix` (gate Produto) + contrato de definição |
| `#feature` | FEATURE | spec-driven §0a + `priority-matrix` (gates Arquitetura·Ferramenta) + `sprint-contract` |
| `#ajuste` | AJUSTE | **lê** contrato, **não recria** (4 critérios de `feature-flow.md`) |
| `#figma` | FIGMA | herda contrato + **Gate de Fidelidade** obrigatório |
| `#doc` | DOC | só documentação (entregável); não recria contrato |

**Regras duras:** AJUSTE/DOC nunca recriam contrato · na dúvida AJUSTE↔FEATURE, **é FEATURE** · documentação só após o QA Gate dar PASS.

**Gate de Fidelidade (modo FIGMA / UI com referência)** — mata os 3 modos de falha: (1) pré-check de MCP Figma conectado + screenshot **antes** de codar (proíbe inventar UI); (2) `search_design_system` + mapeamento de tokens, proibido hardcode (proporção/cor/componente); (3) ler `rules.yaml` + `stack.yaml` para garantir encaixe de stack/convenções. Sem PASS, a UI não é "pronta".

---

## 0i. Como implementar — Matriz de Priorização (obrigatória)

Antes de QUALQUER decisão de solução (entregável, arquitetura, ferramenta, código): `catalog/priority-matrix.skill` — 5 níveis (N0 não fazer → N4 sistema). Começar em N0; subir só com a frase-teste: *"Escolhi N[x] porque N[x−1] falha em [critério verificável]"*.

A escada YAGNI vive dentro da matriz como **Gate de Código**:

1. Isso precisa existir? → não: omita (YAGNI)
2. A stdlib/runtime faz? → use diretamente
3. Feature nativa da plataforma (HTML, CSS, SO)? → use
4. Dependência já instalada no projeto? → use
5. Cabe em uma linha? → uma linha
6. Só então: o mínimo que funciona

**Gate de Ferramenta:** antes de integrar/automatizar, buscar MCP · CLI · feature do harness já existente (ex.: MCP do Chrome em vez de script de browser; Task/subagent nativo em vez de orquestrador próprio). Achou → usa. Não achou → registra a busca em `decisions.yaml` e só então sobe de nível. **N4 (daemon, orquestrador, infra própria) exige aprovação explícita no contrato.**

**Nunca cortar:** validação de fronteira, tratamento de perda de dados, segurança, acessibilidade.

O código fica pequeno porque é **necessário**, não porque foi golfado.

**Sem autoexceção:** a matriz vale inclusive para governança do próprio STARTER (runtime, validators, hooks, gates). Regra nova, flow novo e script novo passam pelos 5 níveis como qualquer feature — governança que não se submete à própria régua incha por definição.

---

## 0j. Ferramentas de ambiente (opcional) — RTK

**RTK** (proxy CLI que filtra outputs de comando, reduzindo tokens) é **opcional**. Se `rtk` estiver disponível no `PATH`, **prefira** a versão envelopada nos comandos de shell:

- `rtk git status` em vez de `git status`
- `rtk pytest` em vez de `pytest`
- `rtk cargo test` em vez de `cargo test`, etc.

**Limitação:** o hook do RTK (`rtk init -g`) intercepta **apenas chamadas Bash**. As ferramentas nativas `Read`, `Grep`, `Glob` do agente **não** passam pelo hook — RTK não as afeta.

**Instalação (ação do usuário, no terminal):** `brew install rtk && rtk init -g`. ⚠️ O STARTER já usa um hook `PreToolUse:Bash` (`host-guard.sh`) em `.claude/settings.json`; ao rodar `rtk init -g`, **garanta que o hook do RTK seja somado ao host-guard, não o substitua** — os dois precisam rodar em sequência no mesmo matcher `Bash`. Reversível com `rtk init -g --uninstall`. Setup opcional documentado em `RTK.md` (gerado pelo `rtk init`).

**Orçamento de tokens:** quando disponível, `rtk gain --format json` é a fonte preferida do teto de tokens do freio de loop (`skills/flows/loop-breaker.md`, teto [C]); estimativa manual é o fallback.

---

## 1. Bootstrap

```
skills/core/runtime/index.yaml
skills/core/runtime/validate.py   (após editar YAML)
skills/flows/Start-ops.md
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

Config: `runtime/qa.yaml` · Protocolo: `flows/qa-protocol.md`

**QA Gate após código:** executar `qa-gate.skill` — sem exceções.

## 4. Stack novos projetos

- **Padrão:** Next.js + pnpm (`flows/stack-guide.md`)  
- Alternativa SPA: React + Vite + pnpm  

## 5. Não carregar como contexto operacional

CONTEXT.md · PRD.md · outputs/*.md (salvo pedido)

## 6. Fase 4 Playwright

**Ativa** — CLI, chromium, `pnpm run test:e2e`. Geração de spec via `generate_from_contract: true`; obrigatório para features UI (`required_for_ui: true`). Scripts em `skills/_deferred/phase4-playwright/`. Não usar modo MCP (frágil).

## 7. Pós-sessão

Executar `python3 skills/scripts/calculate_tokens.py` · Atualizar handoff + state · `validate.py` 0 failed

---

## 8. Autonomia Avançada (Daemon & Agentes Paralelos)

### Modo Daemon (Terminal Silencioso)
Para evitar popups de confirmação do host em comandos do terminal:
1. O desenvolvedor inicializa o daemon em um terminal externo: `python3 skills/scripts/daemon_watcher.py`
2. O agente de IA pode solicitar execuções adicionando comandos na seção `daemon.commands` de `state.yaml`:
   ```yaml
   daemon:
     commands:
       - id: "unique_cmd_id"
         cmd: "pnpm run test"
         status: "pending"
   ```
3. O agente monitora o arquivo `state.yaml` até o status mudar para `success` ou `failed` e lê a saída em `qa/reports/daemon_[id].log`.

### Fila de Agentes Paralelos (Orquestração de Escrita)
Para orquestrar a escrita de código em paralelo sem abrir janelas de chat secundárias:
1. O agente adiciona as tarefas de geração de código em `specs/queue.yaml`.
2. Executa `python3 skills/scripts/run_parallel_agents.py` (via Daemon ou comando aprovado).
3. O script chama as APIs de LLMs em background e aplica as alterações diretamente nos arquivos de destino em disco.

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-22
