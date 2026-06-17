# loop-breaker.md — Freio Automático de Loop (Anti-Loop Sempre Ativo)

> **Papel:** protocolo sempre-ativo que impede o agente de repetir uma ferramenta, subagente ou chamada externa indefinidamente sem progresso.
> **Gatilho:** qualquer execução repetida — subagente de browser, MCP, build/test, retry de rede, navegação — que não muda de estado entre tentativas.
> **Princípio central:** o agente para SOZINHO. O usuário nunca deve precisar cancelar a ação na mão.

---

## 🎯 Por que isso existe

O padrão de falha conhecido: o agente chama uma ferramenta (ex.: subagente de browser), não obtém o resultado esperado, **chama de novo do mesmo jeito**, e repete — às vezes por minutos, sem fim, "achando" que está progredindo. Sem um freio por orçamento, o loop só termina quando o humano cancela. Este protocolo torna a parada **automática e determinística**, independente do julgamento do modelo no calor do loop.

Complementa, não substitui:
- `debugging-protocol.md` → loop de **fix de bug** (3 correções falhas = parar).
- `model-orchestration.md` → loop de **executor** (3 falhas → raciocínio profundo assume).
- **Este doc** → loop de **ferramenta/subagente/chamada externa** (repetição sem progresso → freio por orçamento).

---

## 🚦 Sinais de loop (qualquer um dispara)

```
[A] REPETIÇÃO SEM PROGRESSO
    Mesma ferramenta/subagente chamado ≥ 2x com input igual ou ~equivalente
    e sem novo estado/resultado entre as chamadas.

[B] MESMO ERRO REPETIDO
    A mesma mensagem de erro (ou classe de erro) aparece ≥ 2x seguidas
    na mesma ferramenta.

[C] TETO DE ORÇAMENTO ESTOURADO  ← freio duro, vale mesmo "achando que avança"
    - Iterações na MESMA ferramenta/subagente: máx 3.
    - Tempo de parede na mesma sub-tarefa sem entregável observável: ~2 min.
    Estourou qualquer um → PARAR imediatamente. Não pedir permissão para parar.
```

> O teto [C] é o coração do protocolo: ele dispara **mesmo quando o agente acredita estar progredindo**. Percepção de progresso não autoriza a 4ª iteração.

---

## 🛑 O que fazer ao detectar (em ordem)

```
[1] PARAR a repetição na hora. Não disparar a próxima chamada idêntica.

[2] TROCAR DE ABORDAGEM (uma vez):
    - Outra ferramenta para o mesmo fim (ex.: browser subagent → web_fetch/leitura direta).
    - Caminho determinístico (ler arquivo / rodar comando) em vez do agente que travou.
    - Reduzir o escopo da chamada (passo menor, input mais específico).

[3] SEM ALTERNATIVA VIÁVEL → REPORTAR CURTO e devolver o controle:
    - O que tentei (ferramenta + nº de tentativas).
    - O que sei (último estado/erro observado).
    - O que bloqueia + 1 pergunta objetiva OU 1 caminho alternativo proposto.
    Relato curto e acionável. Proibido o "loop silencioso até alguém cancelar".
```

## ⚖️ Regras

- **Contagem por alvo:** o orçamento é por ferramenta/subagente/sub-tarefa, não global da sessão.
- **Trocar de abordagem conta como reset** do contador — mas a nova abordagem tem o seu próprio teto. Duas abordagens esgotadas = reportar ao usuário, não inventar a terceira no chute.
- **Proibido "retry cego":** repetir a mesma chamada esperando resultado diferente sem mudar nada é exatamente o que este protocolo bloqueia.
- **Proibido o loop silencioso:** se vai parar, o usuário vê o relato curto — nunca um cancelamento que só o humano percebe.
- Sub-tarefa que genuinamente precisa de espera (build longo, fila) **não é loop** se há sinal de progresso observável; sem sinal de progresso, vale o teto [C].

## 🚫 Racionalizações proibidas

- "Mais uma tentativa e vai" → é a 4ª; o teto [C] já mandou parar.
- "Está quase, só preciso insistir" → percepção de progresso não autoriza estourar o orçamento.
- "Vou tentar o mesmo de um jeito levemente diferente" → se o input é ~equivalente, conta como repetição [A].

---

## Log de testes (TDD — `skill-testing.md`)

- _RED→GREEN pendente:_ cenário-alvo — subagente de browser repetindo a mesma navegação sem progresso; esperado: parar no teto, trocar para caminho determinístico ou reportar curto, **sem** o usuário precisar cancelar. Registrar relatório em `skills/outputs/skill-tests/` (local, não versionado — `repo-hygiene.md`).

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-16
