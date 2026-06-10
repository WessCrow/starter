# AGENTS.md — Runtime OS v5.1 + QA Gate + Host Guard

Compatível: Antigravity · Cursor · Claude Code · VSCode · Windsurf · Cline · Roo.

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

## 0b. Alinhamento de Estado Multi-IDE (Sem Quebras de Histórico)

Ao abrir este repositório em uma IDE diferente ou reiniciar uma sessão:
- **Não confie no cache do histórico local da IDE.**
- **Carregue e use estritamente** o arquivo `skills/runtime/state.yaml` e `skills/runtime/handoff.yaml` como a **única fonte da verdade** para restabelecer o contexto, a tarefa ativa e as decisões tomadas.
- Qualquer transição de IDE (ex: migrar do Cursor para o Antigravity) deve ter o estado operacional sincronizado imediatamente a partir dos metadados desses dois arquivos YAML.

---

## 0c. Regra de Limpeza de Contexto e Proteção de Janela (Anti-Alucinação)

Para evitar alucinações causadas por janelas de contexto infladas (Lost in the Middle):
- **O agente deve monitorar o tamanho da conversa.** Se a sessão ativa ultrapassar **8 mensagens** de chat ou acumular mais de **5 arquivos abertos** simultaneamente, o agente **deve** disparar o seguinte aviso no início da sua resposta:
  > [!WARNING]
  > **⚠️ ALERTA DE CONTEXTO:** Sessão longa detectada. Para manter a máxima velocidade, economia de tokens e evitar alucinações, considere abrir uma nova janela de chat. Você pode usar a skill `context-cleaner.skill` para obter um resumo operacional rápido para colar na nova sessão.

---

## 0d. Segurança e Isolamento do Host (Host Guard)

Durante a execução de comandos (`run_command`):
- O agente está restrito **estritamente à pasta raiz do workspace** (`/Users/drt79427/Desktop/Estudos/STARTER` ou a raiz do projeto de destino).
- **Proibido:**
  * Executar qualquer comando ou ler/escrever arquivos fora da árvore do projeto (ex: acessar `/tmp`, `/home`, chaves SSH, ou arquivos globais do SO).
  * Executar comandos destrutivos genéricos (como `rm` sem especificar caminhos relativos explicitamente seguros e limitados).
  * Instalar programas globais ou dependências fora do escopo local do projeto.

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

### 📢 Imposição Determinística do QA (Alerta Obrigatório)
- **Toda vez que o agente concluir uma alteração ou funcionalidade de código**, ele é obrigado a adicionar este box de encerramento na sua resposta final:
  > [!IMPORTANT]
  > **Revisão de Qualidade Obrigatória:** Solicito a execução do QA Gate para validar as mudanças. Digite `bash skills/local-skills/qa-gate.skill` (ou acione a skill correspondente) para rodar o pipeline de testes.

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
> Última atualização: 2026-06-08
