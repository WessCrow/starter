# repo-hygiene.md — O que versionar vs. o que fica local

> **Papel:** política de compartilhamento de arquivos no repositório STARTER (framework) e em projetos filhos  
> **Verificador:** `python3 skills/scripts/check-repo-hygiene.py`  
> **Antes de commit/push:** ver também `gitprotocol.md` Etapa 3

---

## Princípio

O repositório público distribui **framework + documentação para usuários**.  
Artefatos de **sessão, teste, diagnóstico e planejamento interno** ficam **fora do git**.

---

## Estrutura de `docs/`

```
docs/
  README.md           ← índice (versionado)
  public/             ← documentação para quem usa o STARTER (versionado)
  private/            ← só na sua máquina (gitignored, exceto README.md)
```

| Pasta | Versionar? | Exemplos |
|-------|------------|----------|
| `docs/public/` | ✅ Sim | `O-QUE-E-O-STARTER.md`, copy para GitHub, landing |
| `docs/private/` | ❌ Não | relatórios de teste, planos de ação, diagnósticos, PRD interno |

---

## Nunca versionar (lista canônica)

### Pastas inteiras

| Caminho | Motivo |
|---------|--------|
| `_lab/` | Fixtures e testes de execução local |
| `skills/outputs/` | Gerados por sessão de kickoff (exceção no repo framework: 3 seeds `ARCHITECTURE.md`, `PROJECT_BRIEF.md`, `ROADMAP.md`) |
| `skills/cache/` | Cache operacional |
| `qa/reports/` | Relatórios QA por feature (projeto filho) |
| `node_modules/`, `dist/`, `.next/`, `build/` | Build/deps |
| `.pnpm-store/` | Store local pnpm |

### Padrões de nome (em qualquer pasta)

| Padrão | Motivo |
|--------|--------|
| `relatorio-*.md` / `relatorio_*.md` | Relatórios de teste/sessão |
| `plano-acao*.md` / `plano-melhoria*.md` | Planos internos de melhoria |
| `diagnostico.md` | Snapshots de diagnóstico |
| `STARTER-PRD.md` / `STARTER-CONTEXT.md` | Meta-docs do mantenedor (não do usuário) |

**Exceção:** arquivos em `skills/templates/` (são modelos, não artefatos de sessão).

### Arquivos sensíveis

- `.env`, `.env.local`, `*.pem`, `*.key` — ver Host Guard em `validate.py`

---

## Projetos filhos (após “Começar projeto”)

Na raiz do **projeto novo**, também ficam locais (não commitar):

- `CONTEXT.md`, `PRD.md` — gerados na sessão (limpos pelo bootstrap se copiou do framework)
- `specs/` — rastro de feature **do projeto** (versionar no repo **do app**, não no repo STARTER)
- `qa/reports/` — relatórios QA Gate

O repo **STARTER** (framework) não deve conter código de app nem specs de projeto de exemplo.

---

## Comandos

```bash
# Verificar índice git inteiro
python3 skills/scripts/check-repo-hygiene.py

# Só o próximo commit (pre-commit mental)
python3 skills/scripts/check-repo-hygiene.py --staged

# Remover do git sem apagar do disco
git rm --cached docs/private/plano-acao-criticos.md
```

Integrado em `validate-skills.py` (checagem antidrift do sistema) e na CI (`.github/workflows/validate.yml`).

---

## Hook pré-commit (opcional, recomendado)

Para bloquear automaticamente commits com arquivo privado/proibido staged:

```bash
git config core.hooksPath .githooks
```

O hook em `.githooks/pre-commit` roda `check-repo-hygiene.py --staged` a cada commit. Para desativar: `git config --unset core.hooksPath`.

---

## Fluxo recomendado

1. Relatório / plano / diagnóstico → salvar em `docs/private/`
2. Antes de `git commit` → rodar `check-repo-hygiene.py` (ou ativar o hook acima)
3. Documentação para usuário final → `docs/public/` ou `README.md` na raiz

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> Última atualização: 2026-06-10
