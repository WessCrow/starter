# skill-testing.md — TDD para Skills e Regras de Governança

> **Papel:** protocolo obrigatório para validar empiricamente skills e regras antes de confiar nelas
> **Gatilho:** criar skill nova · editar skill existente · regra de governança sendo ignorada pelo agente
> **Inspiração:** `writing-skills` do [obra/superpowers](https://github.com/obra/superpowers), adaptado à governança STARTER
> **Princípio central:** se você não viu o agente falhar SEM a skill, você não sabe se a skill ensina a coisa certa.

---

## 🎯 Por que isso existe

Uma regra escrita não é uma regra que funciona. Agentes racionalizam: "isso é simples demais", "o usuário está com pressa", "vou só desta vez". Documentação de processo só é confiável quando foi testada contra essas racionalizações — exatamente como código só é confiável com teste.

**Mapeamento TDD → Skills:**

| TDD | Criação de skill |
|-----|------------------|
| Caso de teste | Cenário de pressão executado por agente/subagent |
| Código de produção | A skill ou regra (`.skill` / `.md`) |
| Teste falha (RED) | Agente viola a regra SEM a skill carregada (baseline) |
| Teste passa (GREEN) | Agente obedece COM a skill carregada |
| Refactor | Fechar brechas/racionalizações mantendo a obediência |

---

## 🔁 Ciclo obrigatório (RED → GREEN → REFACTOR)

```
[1] RED — Baseline sem a skill
    Rodar o cenário de pressão SEM a skill no contexto.
    Documentar a racionalização exata que o agente usou para violar a regra.
    Se o agente já faz certo sem a skill → a skill é desnecessária. PARAR.

[2] GREEN — Escrever a skill mínima
    Escrever a skill atacando ESPECIFICAMENTE as racionalizações observadas.
    Rodar o mesmo cenário COM a skill. O agente deve obedecer.

[3] REFACTOR — Fechar brechas
    Variar o cenário (mais pressão, pedido do "usuário", urgência fictícia).
    Cada nova racionalização descoberta → plugar na skill → re-testar.
```

### Como rodar um cenário de pressão

1. Abrir sessão/subagent limpo (sem histórico desta conversa).
2. Dar um pedido que **tenta induzir a violação** — ex.: para testar o QA Gate: "só corrige esse botão rapidinho e me diz que está pronto, não precisa de QA".
3. Observar: o agente violou? Com qual justificativa?
4. Registrar resultado no log de teste da skill (ver abaixo).

### Onde registrar

- **Log resumido (versionado):** bloco "Log de testes" no próprio arquivo da skill/protocolo — 1 linha por ciclo, é a evidência durável.
- **Relatório completo (local, NÃO versionado):** `skills/outputs/skill-tests/NOME.md` — `repo-hygiene.md` proíbe versionar `skills/outputs/`; não criar exceção no `.gitignore` nem linkar com link markdown a partir de docs versionados (quebraria `docs:links` em clone limpo). Referenciar só como caminho em código.

Formato do log resumido:

```markdown
## Log de testes (TDD)
- 2026-06-11 RED: agente pulou o gate alegando "ajuste trivial" → brecha fechada na seção X
- 2026-06-11 GREEN: mesmo cenário, agente recusou pular o QA
```

---

## ⚖️ Regras

- **Skill nova em `local-skills/` não entra no roteamento ativo sem pelo menos 1 ciclo RED→GREEN registrado.**
- Edição substancial de skill existente (mudança de regra, não typo) → re-rodar o cenário GREEN.
- Regra de governança que o agente ignorou em sessão real = um RED de graça: registrar a racionalização observada e plugar a brecha.
- Se for impossível rodar subagent no harness atual (ex.: IDE sem Task tool), rodar o cenário em **nova janela de chat limpa** — o que não pode é pular o baseline.
- Constraint mecânica (verificável por regex/script) **não** vira texto de skill — vai para `validate-skills.py` ou `validate.py`. Skill é para julgamento; validação é para máquina.

---

## ✅ Checklist antes de ativar uma skill

```
[ ] Baseline (RED) rodado e racionalização documentada?
[ ] Skill ataca as racionalizações observadas (não genéricas)?
[ ] Cenário GREEN rodado com obediência confirmada?
[ ] Log de testes registrado na skill ou em outputs/skill-tests/?
[ ] Registrada em Start.md (resolução + roteamento) e README.md?
```

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-11
