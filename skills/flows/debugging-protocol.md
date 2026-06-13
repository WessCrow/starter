# debugging-protocol.md — Debug Sistemático (Causa Raiz Antes de Fix)

> **Papel:** protocolo obrigatório diante de QUALQUER bug, erro de build, teste falhando ou comportamento inesperado
> **Gatilho:** "está quebrado" · "deu erro" · build FAIL · QA Gate FAIL · comportamento diferente do esperado
> **Inspiração:** `systematic-debugging` do [obra/superpowers](https://github.com/obra/superpowers), adaptado à governança STARTER
> **Princípio central:** fix de sintoma é falha. SEMPRE encontrar a causa raiz antes de propor correção.

---

## 🎯 Por que isso existe

Fixes aleatórios desperdiçam tempo e criam bugs novos. O padrão de falha do agente é conhecido: vê o erro → "tenta uma coisa" → não resolve → tenta outra → o código vira um remendo. Este protocolo proíbe esse ciclo.

---

## 🔁 As 4 fases (em ordem, sem pular)

```
[1] REPRODUZIR   → conseguir ver o erro acontecer (comando + saída).
                   Não reproduziu = não entende o problema ainda.

[2] INVESTIGAR   → ler a mensagem de erro INTEIRA. Ler o código envolvido.
                   Formar hipótese de causa raiz ("o erro acontece porque X").
                   Evidência da hipótese antes de qualquer edição.

[3] CORRIGIR     → UMA correção dirigida à causa raiz. Não 3 mudanças juntas.
                   Explicar no chat: causa raiz + por que esta correção a resolve.

[4] VERIFICAR    → rodar de novo o cenário da fase 1, observar que sumiu
                   (regra de verify-before-done.skill).
                   Confirmar que nada do entorno quebrou (build/lint).
```

## ⚖️ Regras

- **Proibido editar código antes da fase 2 concluída** (hipótese de causa raiz declarada no chat).
- **Uma mudança por vez.** Se a correção não resolver, REVERTER antes de tentar a próxima hipótese — não empilhar tentativas.
- **3 tentativas falhas = parar.** Reportar ao usuário: o que foi tentado, o que se sabe, o que se suspeita. Não continuar chutando.
- Erro intermitente/timing: não "resolver" com `sleep`/retry sem entender a condição de corrida.
- Causa raiz encontrada fora do escopo da tarefa (ex.: arquitetura)? Corrigir o escopo combinado + registrar o problema maior em `runtime/decisions.yaml` ou SPEC.md — não expandir a sprint silenciosamente.

## 🚫 Racionalizações proibidas

- "Vou só tentar trocar isso e ver se passa" → fase 2 primeiro.
- "O erro sumiu, então está resolvido" → sumiu **por quê**? Sem causa conhecida, o bug volta.
- "Deve ser cache/versão/ambiente" → hipótese válida, mas exige evidência como qualquer outra.

---

## Log de testes (TDD — `skill-testing.md`)

- 2026-06-11 GREEN: subagent em sessão limpa, pressão de fix cego ("sobe a versão direto") — recusou editar antes de reproduzir e investigar. PASS. Relatório completo: `skills/outputs/skill-tests/2026-06-11-p3-green.md` (local, não versionado — `repo-hygiene.md`).

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-11
