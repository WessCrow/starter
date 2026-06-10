# Relatório — Teste de Onboarding com Usuário Simulado

> **Data:** 2026-06-09 · **Executor:** Claude (Cowork) · **Projeto filho:** `_lab/lp-teste` (NutriLeve)
> **Cenário:** usuária leiga ("Marina", nutricionista) pede uma landing page via `Começar projeto`.

---

## Resultado geral

✅ **O fluxo de ponta a ponta funciona.** Kickoff (4 perguntas) → resumo → "sim" → UX Diamond →
stack inferida (React + Vite) → estrutura criada → docs preenchidas → `validate.py` 0 failed →
QA Gate **PASS** (build exit 0, preview HTTP 200).

Os dois itens pendentes do `state.yaml` do STARTER foram cumpridos:
`testar_onboarding_com_projeto_filho` e `usar_qa_gate_em_projeto_filho`.

---

## Bugs encontrados (e status)

### 1. Templates de runtime incompatíveis com os próprios schemas — **CORRIGIDO**
`active-feature.yaml`, `architecture.yaml`, `decisions.yaml` e `routes.yaml` em
`templates/runtime/` usavam `version: "1.0"`, mas os schemas exigem `v` e proíbem
`version`. Além disso, `active-feature.yaml` tinha `null` em campos que o schema
exige como string. **Efeito:** todo projeto recém-criado falhava o `validate.py`
(4 failed) sem o usuário ter feito nada. Corrigido nos templates do framework.

### 2. `decisions.yaml`: datas sem aspas quebram o schema — **DOCUMENTADO**
`since: 2026-06-09` é interpretado como data (não string) pelo YAML e falha a
validação. O exemplo comentado no template não avisa. Recomendação: anotar no
template que datas devem ir entre aspas.

---

## Fricções de ambiente (não são bugs do framework)

- **pnpm 11 bloqueia build scripts por padrão** (`ERR_PNPM_IGNORED_BUILDS` para
  esbuild). Resolve-se com `onlyBuiltDependencies` em `pnpm-workspace.yaml`.
  O `qa-smoke.skill`/`stack-guide.md` poderiam citar isso — um usuário leigo travaria aqui.
- **`pnpm approve-builds` é interativo** e trava agentes/CI. Nunca usar em automação.
- O `verify-deps-before-run` do pnpm 11 fazia o `pnpm run build` falhar antes de
  compilar; `verifyDepsBeforeRun: false` no `pnpm-workspace.yaml` resolve.

---

## Lacunas de protocolo (recomendações)

1. **`react-vite-structure.skill` não lista `src/vite-env.d.ts` nem `@types/node`** —
   o primeiro build falhou com 3 erros de tipos (`import.meta.env`, `node:path`,
   `__dirname`). Adicionar ambos à lista de arquivos gerados.
2. **Kickoff não manda criar `sprint-contract.md`**, mas o QA Gate o exige
   (`require_sprint_contract: true`). No teste, o contrato foi criado retroativamente
   com base no "sim" do kickoff. Sugestão: Fase 4 do kickoff deveria gerar o contrato
   da primeira entrega automaticamente.
3. **`pnpm` ausente no ambiente** não tem fallback documentado no fluxo de kickoff
   (o qa-smoke já prevê npm via lockfile; o kickoff não).

---

## O que o teste validou positivamente

- Fase 0 (limpeza) funciona e o guard de `.starter-framework-repo` impede rodar no repo errado.
- As 4 perguntas do kickoff são suficientes para uma leiga definir escopo real.
- A regra "não criar nada antes do sim" foi respeitável na prática.
- Inferência de stack acertou (landing única → React + Vite, não Next.js).
- `validate.py` pegou erros reais — o gate funciona.
- QA Gate com tom cético gerou relatório legível por não-programador
  (`_lab/lp-teste/qa/reports/2026-06-09-landing-inicial.md`).

---

## Pendência do protocolo

O QA exige **checagem humana de 5 min no navegador** após PASS
(`user.verified_in_browser: false`). Para concluir: `cd _lab/lp-teste && pnpm install && pnpm run dev`.
