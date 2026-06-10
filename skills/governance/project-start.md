# project-start.md — Protocolo de Inicialização de Projetos

> **Papel:** Protocolo obrigatório para criação de novos projetos  
> **Ativado por:** após **"sim"** no `governance/kickoff.md` (comando *Começar projeto*)  
> **Antes deste arquivo:** kickoff — perguntas + confirmação  
> **Governança de capability:** `governance/skills-governance.md`
> **Depende de:** `runtime/rules.yaml` · `templates/runtime/` · structure/

---

## 🎯 Objetivo

Garantir que todo novo projeto seja iniciado com:
- `runtime/rules.yaml` ativo desde o primeiro commit
- Design System declarado em `runtime/context.yaml` antes do primeiro componente
- estrutura de arquivos consistente com a stack
- `skills/runtime/*.yaml` criado como fonte operacional da IA
- `CONTEXT.md` humano leve (≤50 linhas) na raiz
- governance aplicada desde o início

---

## 🔁 Fluxo Completo

```
[1] Copiar templates/runtime/ → skills/runtime/ (inclui schema/ + index.yaml + validate.py)
        ↓
[2] Capturar intenção e extrair parâmetros do projeto
        ↓
[3] ★ CAMADA ESTRUTURAL ★
    Detectar stack → structure skill → pastas + stack.yaml
        ↓
[4] Preencher runtime/*.yaml (context, stack, state, decisions, routes)
        ↓
[5] Criar CONTEXT.md humano na raiz (≤50 linhas, espelho leve)
        ↓
[6] Skill funcional: project-starter
        ↓
[7] PRD.md + outputs/ (documentação humana)
        ↓
[8] Entregar projeto pronto para evolução
```

---

## [1] Capturar Intenção

Antes de criar qualquer arquivo, responder:

- **O que** o projeto deve fazer?
- **Para quem** (audiência, usuário final)?
- **Qual escopo** (MVP, protótipo, produto final)?
- **Quais restrições** (tecnologia, prazo, equipe)?
- **Qual o resultado esperado** desta sessão?

Se houver ambiguidade: assumir a interpretação mais provável e explicitar na documentação.

---

## [2] Extrair Parâmetros

Estrutura de parâmetros mínimos:

```
nome do projeto:
objetivo principal:
audiência:
escopo desta sessão:
tecnologias (se definidas):
restrições conhecidas:
referências visuais (se existirem):
```

---

## [3] Camada Estrutural — Obrigatória

Esta etapa acontece **antes** de qualquer skill funcional.

### 3a. Detectar stack

Extrair do pedido ou perguntar se não estiver claro:
- Tipo: frontend / backend / monorepo / fullstack?
- Framework: React? Next.js? Node.js? outro?
- Padrão arquitetural: Clean Architecture? simples?

### 3b. Selecionar e executar structure skill

| Stack detectada | Skill a executar |
|---|---|
| React + Vite | `structure/react-vite-structure.skill` |
| Next.js | `structure/nextjs-structure.skill` |
| Backend / API | `structure/backend-structure.skill` |
| Monorepo | `structure/monorepo-structure.skill` |
| Design System | `structure/design-system-structure.skill` |
| Clean Architecture / DDD | `structure/clean-architecture.skill` |
| Frontend genérico | `structure/frontend-structure.skill` |

### 3c. Criar arquitetura de pastas

Executar a structure skill selecionada:
- Criar todas as pastas definidas na skill
- Gerar arquivos de configuração raiz (tsconfig, vite.config, etc.)
- Criar boilerplates de entrada (main.tsx, app.ts, index.ts)
- Registrar em `outputs/ARCHITECTURE.md` qual skill foi usada e por quê

---

## [4] Selecionar Skill Funcional

Consultar `Start.md` + `governance/skills-governance.md`:

1. Verificar `local-skills/project-starter.skill`
2. Se não disponível → parar e corrigir o catálogo / roteamento local
3. Não usar `linked-skills/` ou `skills.sh` como fallback operacional nesta fase

---

## [5] Gerar Estrutura de Documentação

A estrutura mínima de documentação de um projeto é:

```
/projeto
├── README.md
├── CONTEXT.md              → humano, ≤50 linhas
├── PRD.md                  → humano, especificação
├── skills/runtime/*.yaml   → operacional IA ← carregado toda sessão
├── [código — structure skill]
└── skills/outputs/         → ROADMAP, BRIEF, ARCHITECTURE (humano)
```

Templates:
- `templates/runtime/`       → skills/runtime/*.yaml
- `context-template.md`      → CONTEXT.md humano
- `prd-template.md`          → PRD.md
- `briefing-template.md`     → para PROJECT_BRIEF
- `roadmap-template.md`      → para ROADMAP
- `architecture-template.md` → para ARCHITECTURE

---

## [6] Popular Outputs Obrigatórios

### PROJECT_BRIEF.md
Preencher com:
- nome e objetivo do projeto
- contexto e problema que resolve
- audiência e casos de uso
- escopo atual e próximos passos
- data de criação

### ROADMAP.md
Preencher com:
- fase atual (ex.: Fase 1 — Estrutura Base)
- itens em progresso
- próximos marcos
- itens futuros / backlog

### ARCHITECTURE.md
Preencher com:
- decisões técnicas tomadas
- stack escolhida (se definida)
- padrões de estrutura adotados
- integrações previstas
- restrições arquiteturais

---

## [7] Registrar Decisões

Toda decisão relevante deve ser registrada em `ARCHITECTURE.md`:

```markdown
## Decisão: [nome da decisão]
**Data:** YYYY-MM-DD  
**Contexto:** Por que esta decisão foi necessária  
**Decisão:** O que foi escolhido  
**Consequências:** O que isso implica no projeto  
```

---

## [8] Checklist de Entrega

Antes de considerar o projeto inicializado:

- [ ] `skills/runtime/` + `schema/` criados de `templates/runtime/`
- [ ] `python3 skills/runtime/validate.py` → 0 failed
- [ ] `runtime/index.yaml` com load_order hot/warm/cold
- [ ] Stack detectada → `runtime/stack.yaml`
- [ ] Structure skill executada
- [ ] `.env.example` na raiz (placeholders — sem valores reais; `.env.local` no `.gitignore`)
- [ ] `CONTEXT.md` humano na raiz (≤50 linhas)
- [ ] `sprint-contract.md` na raiz (se kickoff incluiu UI — aprovado na Fase 2)
- [ ] `PRD.md` criado
- [ ] Decisões em `runtime/decisions.yaml`
- [ ] Nenhum componente criado que já existe no Design System
- [ ] Código inicial não viola nenhuma regra do RULES.md
- [ ] Governance verificada (gitprotocol se houver versionamento)
- [ ] Estrutura de arquivos coerente com o escopo

---

## 🔄 Evolução Contínua

A cada interação subsequente com o projeto:

1. Ler `outputs/` para restaurar contexto
2. Identificar o que mudou desde a última sessão
3. Executar alteração preservando padrões existentes
4. Atualizar o output relevante (brief / roadmap / architecture)
5. Manter consistência entre os três documentos

O projeto nunca começa do zero em uma segunda sessão.  
O contexto está sempre em `outputs/`.

---

## ⚠️ Anti-padrões

- Criar projeto sem preencher ao menos PROJECT_BRIEF
- Ignorar templates disponíveis em `/templates`
- Sobrescrever outputs de sessões anteriores sem preservar histórico
- Iniciar sem identificar escopo da sessão atual
- Tratar capability futura como fallback operacional de kickoff

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07
