# Start-ops — Runtime Orchestrator

> **v5.1** · Runtime OS + **QA Gate** · Referência: `Start.md`

---

## 0. Comando **Começar projeto**

Gatilho do usuário → `governance/kickoff.md` (perguntas → resumo → **sim** → criar).  
Não exigir stack. Ver `COMECAR-PROJETO.md`.

---

## 0b. Bootstrap (sessão normal)

```txt
1. runtime/index.yaml
2. validate.py (se runtime editado)
3. HOT → rules, context, state
4. WARM → handoff, qa, active-feature (+ SPEC se software)
5. Start-ops (este arquivo)
```

---

## 1. Carregamento (`index.yaml`)

### Hot — sempre

`rules.yaml` · `context.yaml` · `state.yaml`

### Warm — feature / pós-implementação

| Arquivo | Quando |
|---------|--------|
| `handoff.yaml` | Retomar sessão ou após QA |
| `qa.yaml` | Antes/depois de implementar |
| `active-feature.yaml` | Feature ativa |
| `SPEC.md` | Software com feature scope |

### Cold — lazy

`routes` · `architecture` · `decisions` · `stack`

**Docs humanos:** `qa-protocol.md` · `stack-guide.md` (sob demanda)

---

## 2. Fluxo com QA Gate (obrigatório)

```txt
Pedido → Especialista que Pergunta → confirmação
      → sprint-contract.md (usuário aprova)
      → IMPLEMENTAR (Builder)
      → ★ qa-gate.skill (+ qa-smoke)
      → PASS? → usuário testa 5 min no browser → handoff qa.pass
      → FAIL? → corrigir → qa-gate de novo
```

### Gate rígido

- **Proibido** marcar feature/SPEC como concluída se `handoff.qa.last_status != pass`
- **Proibido** PASS sem sprint-contract verificado
- Relatório em português simples → `qa/reports/`

---

## 3. Stack novos projetos

Ler `governance/stack-guide.md`:

- **Padrão disruptivo:** Next.js + TS + Tailwind + shadcn + **pnpm**
- **SPA rápida:** React + Vite + mesma base
- npm ok se projeto já usa `package-lock.json`

---

## 4. Skills

| Momento | Skill |
|---------|-------|
| Após implementar | `qa-gate` → `qa-smoke` |
| UI só revisão | `ux-audit` (secundária) |
| Direção visual inicial / referências vagas | `visual-direction-brief` |
| Referência concreta / site / screenshot | `web-design-cloner` |
| Motion, fluidez e microinterações | `fluid-ui-review` → `fluid-ui-implementation` → `fluid-ui-snippets` |
| Curadoria de skill externa / marketplace / MCP | `marketplace-curator` |
| Vídeo HTML / HyperFrames | `hyperframes` |
| Preview / render / lint / inspect HyperFrames | `hyperframes-cli` |
| TTS / transcript / cutout HyperFrames | `hyperframes-media` |
| Novo projeto | structure → `project-starter` |
| Roteamento | cold `routes.yaml` |

---

## 5. Pós-sessão

1. Atualizar YAML  
2. `validate.py` → 0 failed  
3. `handoff.yaml` + `state.yaml`  
4. Lembrete: Fase 4 Playwright em `handoff.reminders` / ROADMAP

---

## 6. Fluxo resumido

```txt
index → validate → hot → warm → implement → QA GATE → persist
```

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07
