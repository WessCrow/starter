# AGENTS.md — Runtime OS v5.1 + QA Gate

Compatível: Cursor · Claude Code · VSCode · Windsurf · Cline · Roo · Antigravity.

---

## 0. Novo projeto — comando único

Se o usuário disser **`Começar projeto`** (ou equivalente):

1. **`bash skills/scripts/clean-framework-artifacts.sh`** — Fase 0 (ver `bootstrap-cleanup.md`)
2. Ler `skills/governance/kickoff.md`
3. Fazer até **4 perguntas** em português simples (uma por vez)
3. Resumir + **"Posso começar?"** — **não criar arquivos antes do sim**
4. Após sim → `project-starter.skill` + `project-start.md`

O usuário **não** precisa citar stack. Ver `COMECAR-PROJETO.md` na raiz.

**Bootstrap:** colar `skills/` + `AGENTS.md`. Limpeza do framework é **automática** no passo 1 acima.

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

1. Existe `sprint-contract.md` aprovado pelo usuário  
2. Executar `qa-gate.skill` (tom **cético**, relatório **PT-BR simples**)  
3. `qa-smoke.skill` — `pnpm run build` (ou `npm` se lock npm)  
4. **FAIL** → não marcar feature pronta; listar correções claras  
5. **PASS** → pedir usuário testar 5 min no navegador  

Config: `runtime/qa.yaml` · Protocolo: `governance/qa-protocol.md`

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
> Última atualização: 2026-06-07
