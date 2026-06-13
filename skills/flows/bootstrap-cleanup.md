# bootstrap-cleanup.md — Limpeza automática (Fase 0)

> **Quando:** no comando **Começar projeto**, **antes** da pergunta 1  
> **Quem:** o agente — o usuário **não** precisa apagar nada manualmente

---

## Objetivo

Evitar mistura entre o projeto **STARTER** (framework) e o **app novo**.

---

## Executar primeiro (obrigatório)

Rodar na **raiz do projeto novo** (preferido):

```bash
cd /caminho/do/meu-app
bash skills/infra/scripts/clean-framework-artifacts.sh
```

O script usa o diretório atual (`pwd`), não o repositório STARTER.

Ou apagar manualmente os mesmos caminhos (se script falhar).

---

## O que APAGAR

| Caminho | Motivo |
|---------|--------|
| `CONTEXT.md` (raiz) | Quase sempre é cópia/meta do STARTER |
| `PRD.md` (raiz) | Idem |
| `skills/core/runtime/` (pasta inteira) | YAML do framework copiado |
| `skills/outputs/` (pasta inteira) | ROADMAP/BRIEF do STARTER |

---

## O que NUNCA apagar

| Caminho | Motivo |
|---------|--------|
| `skills/flows/` | Protocolos (kickoff, QA, etc.) |
| `skills/catalog/` | Skills |
| `skills/templates/` | Boilerplates do **novo** projeto |
| `skills/structure/` | Structure skills |
| `skills/_deferred/` | Rascunhos |
| `skills/infra/scripts/` | Scripts de bootstrap |
| `AGENTS.md` (raiz) | Instruções genéricas do agente |
| `COMECAR-PROJETO.md` | Lembrete (opcional) |
| Código do app (`src/`, `app/`, etc.) | Só se já existir app real — ver exceção |

---

## Exceção — continuar projeto existente

Se o usuário disser explicitamente **"continuar projeto"** / **"não é projeto novo"**:

- **Não** rodar cleanup
- **Não** apagar `skills/core/runtime/` nem CONTEXT/PRD do app
- Seguir fluxo de sessão normal (`Start-ops`)

---

## Depois da limpeza (obrigatório antes de codar)

A Fase 0 remove `skills/core/runtime/`. Links em `skills/INDEX.md` ficam inválidos até restaurar o runtime do **novo** projeto.

1. Confirmar em uma linha: *"Limpei artefatos do framework; vamos definir seu app."*
2. Seguir `kickoff.md` → perguntas → "Posso começar?"
3. Após **"sim"**: `project-start.md` **[1]** — copiar `skills/templates/runtime/` → `skills/core/runtime/` (não pular)
4. **Proibido** implementar código do app antes do passo 3 em projeto novo

Pilotos em `_lab/`: mesma regra — ver `docs/private/plano-sprint-006-fechamento.md` (roteiro 7 passos).

---

## Mensagem ao usuário (template)

> Removi automaticamente arquivos do template STARTER que poderiam confundir o agente (CONTEXT, PRD e pastas runtime/outputs antigas).  
> Seu **AGENTS.md** e a pasta **skills/** de ferramentas foram mantidos.

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07
