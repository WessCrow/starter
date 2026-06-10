# Plano de Ação — Problemas Críticos do STARTER

> **Data:** 2026-06-09 · **Base:** teste de onboarding (`relatorio-teste-onboarding.md`) + críticas pós-atualização
> **Regra do plano:** nenhuma feature nova entra antes de P0 e P1 zerados.

---

## P0 — Crítico (quebra confiança ou segurança; resolver antes de qualquer outra coisa)

### 1. Corrigir `check_security_leaks()` no validate.py (template + raiz)
**Problema:** dois falso-negativos graves — (a) sem `.gitignore`, nenhum alerta é emitido (caso mais perigoso); (b) `"env" not in content` faz `venv/` silenciar o alerta de `.env` exposto.
**Ação:**
- Inverter a lógica: `.env` existe + `.gitignore` ausente → **alerta máximo**.
- Checar padrão real (linha `.env` ou `*.env` ou `.env*`), não substring solta.
- Excluir `node_modules/` e `.venv/` também da varredura de `.env`.
**Aceite:** 4 casos de teste manuais — (sem gitignore / gitignore com só `venv/` / gitignore correto / sem .env) — com resultado esperado documentado no topo da função.
**Esforço:** ~30 min.

### 2. `react-vite-structure.skill` gera projeto que não compila
**Problema:** faltam `src/vite-env.d.ts` e `@types/node` na lista de arquivos/deps — primeiro build falha com 3 erros de tipos.
**Ação:** adicionar ambos à seção "Arquivos Raiz Gerados" e às devDependencies do boilerplate.
**Aceite:** projeto recém-gerado compila com `pnpm run build` exit 0 sem intervenção.
**Esforço:** ~15 min.

### 3. Kickoff não gera sprint-contract da primeira entrega
**Problema:** QA Gate exige `sprint-contract.md` aprovado (`require_sprint_contract: true`), mas o kickoff nunca o cria → todo primeiro QA é bloqueado ou vira papelada retroativa.
**Ação:** na Fase 4 do `kickoff.md`, após o "sim", gerar `sprint-contract.md` automaticamente a partir do resumo aprovado (o "sim" do resumo = aprovação do contrato). Documentar essa equivalência.
**Aceite:** fluxo kickoff → QA Gate roda sem criar nada manualmente fora do protocolo.
**Esforço:** ~30 min.

---

## P1 — Alto (quebra portabilidade ou credibilidade)

### 4. Caminhos absolutos no `ux-diamond.skill`
**Problema:** links `file:///Users/drt79427/...` e um path `.gemini/antigravity-ide/brain/...` de outra máquina — quebrado para qualquer outro usuário.
**Ação:** trocar todos por caminhos relativos (`skills/local-skills/ux-audit.skill` etc.); remover a referência externa ao brain do Antigravity. Varredura geral: `grep -rn "file:///\|/Users/" skills/` deve retornar zero.
**Aceite:** grep limpo em todo o repo (exceto docs históricas).
**Esforço:** ~20 min.

### 5. README promete o que não tem evidência
**Problema:** "até 80% de economia de tokens" (nunca medido) e "60 segundos" (refutado no teste) expõem o projeto a perda de credibilidade imediata com o público leigo que ele atrai.
**Ação (duas opções, escolher uma):**
- **(a) Medir:** rodar o mesmo kickoff com e sem framework, contar tokens, publicar o número real.
- **(b) Reescrever:** trocar números por benefícios verificáveis ("contexto enxuto por design", "setup guiado em minutos").
**Aceite:** nenhuma afirmação quantitativa sem medição publicada. Aplicar em `README.md` **e** `docs/lp-github.md`.
**Esforço:** (b) ~30 min; (a) ~2 h.

### 6. Sem caminho de upgrade para projetos filhos
**Problema:** template do `validate.py` evoluiu; projeto criado ontem ficou com versão antiga. Cada melhoria abandona os projetos existentes.
**Ação mínima viável:** criar `skills/scripts/upgrade-from-starter.sh` que copia `templates/runtime/validate.py` + `schema/` (nunca os `.yaml` preenchidos) para um projeto filho, com diff antes de aplicar. Registrar versão do framework em `runtime/state.yaml` (`framework_v`).
**Aceite:** rodar o script em `_lab/lp-teste` atualiza o validate.py sem tocar nos dados; `validate.py` continua 0 failed.
**Esforço:** ~1 h.

---

## P2 — Médio (fricção real, mas com workaround)

### 7. pnpm 11 trava usuário leigo
**Ação:** no `stack-guide.md` e `qa-smoke.skill`, documentar: `onlyBuiltDependencies` + `verifyDepsBeforeRun: false` no `pnpm-workspace.yaml`; proibir `pnpm approve-builds` (interativo, trava agente). Incluir o snippet pronto no boilerplate das structure skills.
**Esforço:** ~30 min.

### 8. Armadilha de data no `decisions.yaml`
**Ação:** comentário no template: datas **entre aspas** (`since: "2026-06-09"`), senão o YAML vira `date` e falha o schema.
**Esforço:** ~5 min.

### 9. Feature-flow nunca executado
**Problema:** mesmo padrão que o kickoff tinha — protocolo escrito sem teste real.
**Ação:** repetir o método do teste de onboarding: usuário simulado pede uma feature no NutriLeve (ex.: seção de depoimentos) seguindo `feature-flow.md` de ponta a ponta, incluindo Analyze e constitution check. Registrar relatório em `docs/`.
**Aceite:** ciclo completo specify → QA PASS com rastro em `_lab/lp-teste/specs/001-*/`.
**Esforço:** ~1 sessão.

### 10. Higiene de git
**Problema:** 15 arquivos modificados + 6 não rastreados sem commit — viola o próprio `gitmaster`.
**Ação:** commits separados por tema (fix templates / feature-flow / relatórios / _lab como teste ou no .gitignore — decidir se `_lab/` e `.pnpm-store/` entram no repo; recomendado: ignorar `.pnpm-store/`, manter `_lab/` como fixture de teste).
**Esforço:** ~20 min.

---

## Fora deste plano (estrutural, discutir antes)

- **Independência do QA:** o mesmo modelo se autoavalia. Mitigação real exigiria segundo agente/modelo como avaliador — mudança de arquitetura, não patch.
- **Sobreposição de skills** (3 fluid-ui, 4 scroll): consolidação exige decisão de produto, não correção.

## Ordem de execução sugerida

P0.1 → P0.2 → P0.3 → P1.4 → P1.5(b) → P2.8 → P2.7 → P1.6 → P2.10 → P2.9 (validação final do conjunto).
Critério de saída: novo teste simulado de ponta a ponta (kickoff + feature-flow) passa sem nenhuma intervenção manual fora dos protocolos.
