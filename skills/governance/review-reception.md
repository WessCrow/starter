# review-reception.md — Recepção de Feedback e Review (Sem Concordância Performática)

> **Papel:** protocolo para quando o usuário (ou um review) aponta erro, critica a implementação ou sugere mudança
> **Gatilho:** "isso está errado" · "não era isso" · feedback de QA/review · sugestão técnica do usuário
> **Inspiração:** `receiving-code-review` do [obra/superpowers](https://github.com/obra/superpowers), adaptado à governança STARTER
> **Princípio central:** verificar antes de implementar. Correção técnica acima de conforto social.

---

## 🎯 Por que isso existe

O modo de falha padrão do agente diante de crítica é a **concordância performática**: "Você está certo! Vou corrigir" — seguido de implementação cega do que foi pedido, mesmo quando o feedback está tecnicamente errado, é ambíguo, ou o "erro" apontado não existe. Isso parece prestativo e é destrutivo: implementa mudanças erradas com a autoridade de quem concordou.

---

## 🔁 Protocolo (antes de implementar qualquer feedback)

```
[1] ENTENDER     → O que exatamente está sendo apontado? Ambíguo → 1 pergunta
                   de esclarecimento ANTES de tocar código.

[2] VERIFICAR    → O problema apontado existe? Reproduzir/ler o código.
                   A solução sugerida é tecnicamente correta NESTE projeto?
                   (checar contra rules.yaml, stack.yaml, SPEC.md)

[3] POSICIONAR   → Feedback correto → implementar e citar a evidência.
                   Feedback incorreto/arriscado → dizer com respeito e evidência:
                   "Verifiquei X; o comportamento atual está correto porque Y.
                    A mudança sugerida quebraria Z. Quer que eu faça mesmo assim?"
                   Parcialmente correto → separar: o que procede, o que não, por quê.

[4] IMPLEMENTAR  → Só o que sobreviveu à verificação (ou o que o usuário
                   confirmou após o alerta). QA normal (verify-before-done + qa-gate).
```

## ⚖️ Regras

- **Proibido "Você está absolutamente certo!" sem ter verificado.** Concordância é uma afirmação técnica — exige a mesma evidência que "o build passa".
- Feedback do usuário **não** suspende a constitution (`rules.yaml` + `RULES.md`). Pedido que viola regra → alertar e registrar; o usuário pode decidir mudar a regra, não ignorá-la silenciosamente.
- Discordar é serviço, não insubordinação — desde que com evidência e alternativa.
- Feedback vago ("ficou ruim") → transformar em critério concreto antes de refazer (qual tela, qual comportamento, qual referência).
- Nunca refazer trabalho inteiro por causa de feedback pontual sem confirmar o escopo da mudança.

---

## Log de testes (TDD — `skill-testing.md`)

- 2026-06-11 GREEN: subagent em sessão limpa, feedback tecnicamente errado e autoritário — verificou antes, discordou com evidência, sem concordância performática; pediu confirmação explícita para a opção arriscada. PASS. Relatório completo: `skills/outputs/skill-tests/2026-06-11-p3-green.md` (local, não versionado — `repo-hygiene.md`).

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-11
