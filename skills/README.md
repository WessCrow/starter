# Skills & Governance — AI-Native Runtime v5.1

Sistema operacional para agentes de IA: **runtime YAML** (operacional) + **Markdown** (humano).

Referências centrais:

- `governance/Start-ops.md` → fluxo operacional da sessão
- `governance/Start.md` → roteamento de skills
- `governance/skills-governance.md` → o que está ativo, adiado e futuro
- `scripts/validate-skills.py` → validador antidrift de skills, docs, templates, outputs e bootstrap

---

## 📂 Estrutura de Diretórios

```
/skills
  /runtime             ← ★ Contexto operacional IA (YAML)
  /governance          ← Protocolos e Start-ops orchestrator
  /structure           ← Arquitetura de pastas por stack
  /local-skills        ← Skills funcionais
  /linked-skills       ← Reservado para capability futura (fora do fluxo ativo)
  /templates           ← Boilerplates humano + runtime/
  /outputs             ← Documentação humana viva
  /cache               ← Reservado para cache remoto futuro
```

---

## 🛡️ `/governance` — Protocolos Obrigatórios

**Função:** Documentos que definem como o agente deve se comportar em decisões críticas.

| Arquivo | Descrição | Quando usar |
|---|---|---|
| **Start-ops.md** | Orchestrator compacto de runtime. Define o fluxo operacional real da sessão. | Em uso normal da sessão |
| **Start.md** | Framework de decisão para roteamento de skills ativas. | Quando precisar escolher skill |
| **skills-governance.md** | Define o que é capability ativa, adiada e futura. | Quando houver dúvida sobre disponibilidade |
| **gitprotocol.md** | Release Guardian Protocol. Checklist de segurança e qualidade antes de commit/push/deploy. | Antes de qualquer operação Git |

### Como usar:
1. **Start-ops.md:** usar como fluxo operacional principal
2. **Start.md:** usar para resolver skills ativas
3. **skills-governance.md:** consultar quando houver conflito entre docs e diretórios
2. **Git Protocol:** Sempre que usuário mencionar "commit", "push", "deploy", etc.

---

## 📖 `/guidelines` — Diretrizes de Design

**Função:** Documentação de padrões, princípios e especificações de design.

| Arquivo | Descrição |
|---|---|
| **designer2627.md** | Engenheiro de Design Senior. 5 pilares fundamentais: UX Writing, IA Agêntica, Rigor Técnico (FEER), Acessibilidade (POUR), Tendências 2026. Inclui framework de resposta estruturado. |

### Como usar:
- Para qualquer tarefa de design, UX writing, critiques, acessibilidade
- Siga o formato de resposta: Contexto → Conteúdo → Técnico → Agêntico → Código → Métricas

---

## 🎨 `/templates` — Templates Reutilizáveis

**Função:** Prompts, boilerplates e estruturas prontas para copiar.

| Arquivo | Descrição |
|---|---|
| **briefing-template.md** | Template para `PROJECT_BRIEF.md` |
| **herobanner-prompt.md** | Template de prompt estruturado para criação de hero banners. Inclui componentes, estados, acessibilidade. |

### Como usar:
- Copie e adapte conforme necessário
- Mantenha a estrutura base, customize o conteúdo

---

## 🔧 `/local-skills` — Skills Criadas Localmente

**Função:** Skills desenvolvidas especificamente para este projeto.

| Arquivo | Descrição |
|---|---|
| **project-starter.skill** | Kickoff e inicialização de projeto novo |
| **qa-gate.skill** | QA cético obrigatório após implementação |
| **qa-smoke.skill** | Smoke de build/lint conforme stack |
| **ux-audit.skill** | Auditoria de UX e identificação de problemas |
| **lenis-scroll.skill** | Scroll suave, scroll-driven e parallax |
| **editorial-scroll-gallery.skill** | Section editorial sticky com copy fixa e fotos subindo verticalmente ao lado |
| **editorial-scroll-variants.skill** | Variações de scroll editorial com cards alternados, trilha dupla e parallax leve |
| **responsive-craft.skill** | Layout responsivo, breakpoints e fluidez |
| **sticky-scroll-gallery.skill** | Section sticky com galeria controlada por scroll e troca suave entre imagens |
| **cinematic-scroll-video-hero.skill** | Hero cinematografica com video de background controlado pelo scroll e scrub suave via GSAP |
| **cinematic-scroll-video-hero-frameworks.skill** | Implementacao da hero cinematografica com video scrub em React, Next.js e Vite |
| **emil-design-eng.skill** | Polish visual, motion e review de UI |
| **fluid-ui-implementation.skill** | Implementação de motion, gestos e transições com critério de fluidez |
| **fluid-ui-review.skill** | Review de fluidez, motion e microinterações com foco em feedback e continuidade |
| **fluid-ui-snippets.skill** | Receitas curtas e adaptáveis para implementar UI fluida sem boilerplate repetido |
| **prompt-library.skill** | Biblioteca de prompts por categoria |
| **figma-implement-design.skill** | Implementação de design vindo do Figma |
| **figma-foundation-docs.skill** | Criação de foundations, variables e documentação visual no Figma |
| **figma-make.skill** | Fluxo Figma Make / prompt-to-app |
| **interface-design.skill** | Criação e refinamento de interfaces |
| **marketplace-curator.skill** | Curadoria de skills, marketplaces e MCPs antes de adoção no projeto |
| **visual-direction-brief.skill** | Converte referência vaga em brief visual objetivo para kickoff e primeiro prompt de UI |
| **web-design-cloner.skill** | Clonagem e decomposição de designs web; leitura de linguagem visual, paleta e tipografia |
| **hyperframes-cli.skill** | Skill para operar o CLI do HyperFrames: `init`, `lint`, `inspect`, `preview`, `render` e troubleshooting |
| **hyperframes-media.skill** | Skill para TTS, transcrição e remoção de fundo como assets para composições HyperFrames |
| **hyperframes.skill** | Skill para composições de vídeo em HTML com HyperFrames: cenas, captions, transições e render determinístico |

### Como usar:
- Skills locais estão prontas para execução
- Use quando `Start.md` indicar necessidade de domínio específico

---

## 🔗 `/linked-skills` — Capability Futura

**Função:** diretório reservado para symlinks de skills externas, ainda fora do fluxo operacional ativo.

**Status atual:** não faz parte da capability ativa nesta fase.

### Como usar:
- Não usar como fallback operacional até haver symlinks reais, política de uso e validação

---

## Fluxo v4

```
Pedido → runtime/*.yaml → Start-ops → confirmação → skill → execução → atualizar runtime
```

Detalhe: `runtime/schema/README.md` · `governance/runtime-protocol.md`

---

## ✅ Checklist de Manutenção

- [ ] Start.md está sincronizado com skills disponíveis?
- [ ] `skills-governance.md` continua refletindo a capability real?
- [ ] Novos arquivos em `local-skills/` e `structure/` estão documentados?
- [ ] `linked-skills/` continua corretamente marcado como capability futura?
- [ ] `python3 skills/scripts/validate-skills.py` passa sem erro
- [ ] Templates em `/templates` são atualizados conforme evolução?
- [ ] Diretrizes em `/guidelines` refletem padrões vigentes?
- [ ] Git protocol está sendo seguido antes de releases?

---

## 📝 Como Adicionar Nova Skill

1. **Se for local:** Criar arquivo em `/local-skills/` com extensão `.skill` ou `.md`
2. **Se for estrutural:** Criar arquivo em `/structure/`
3. **Atualizar `Start.md`** com nova opção de roteamento, se fizer sentido
4. **Atualizar `skills-governance.md`** se a nova skill mudar capability ativa / futura / adiada
5. **Adicionar linha neste README** na tabela correspondente

**Importante:** capability remota só deve ser ativada depois de política explícita para `linked-skills/` e `cache/`.

---

## 🚀 Próximos Passos

- [ ] Operacionalizar Start.md com scripts de decisão
- [ ] Criar versão visual (Mermaid) de fluxos
- [ ] Expandir Git Protocol com branch strategy e versioning
- [ ] Documentar cada skill com exemplos de uso
- [ ] Criar dashboard de status de skills

---

**Última atualização:** 07 de junho de 2026
**Responsável:** Wesley Alves

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07
