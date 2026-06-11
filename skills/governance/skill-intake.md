# skill-intake.md — Pipeline de Incubação de Skills (TESTAR_)

> **Papel:** processo obrigatório para avaliar, testar, refinar e assimilar (ou rejeitar) skills depositadas pelo mantenedor
> **Entrada:** `docs/private/_novas skills/` — arquivos com prefixo `TESTAR_`
> **Gatilhos:** comando do mantenedor ("avaliar novas skills") · lembrete do `session-start-hook.sh` quando houver `TESTAR_*` na pasta
> **Princípio central:** rejeitar também é resultado válido. Skill assimilada sem teste é passivo, não ativo.

---

## Convenções da pasta de entrada

| Prefixo | Significado |
|---------|-------------|
| `TESTAR_*` | Candidata aguardando avaliação — único gatilho do pipeline |
| `REJEITADA_*` | Avaliada e rejeitada — motivo no topo do arquivo; não reavaliar sem pedido |
| sem prefixo | Ignorar (rascunho do mantenedor) |

Limite de fila sugerido: **8 candidatas**. Acima disso, triagem agressiva antes de qualquer teste.

---

## Funil (6 etapas — ordem obrigatória)

```
[1] TRIAGEM   → ler a candidata inteira; mapear overlap com skills ativas
                (Start.md → roteamento por intenção) e com OUTRAS candidatas
                da fila. Sobreposição entre candidatas → consolidar em 1 antes
                de prosseguir (a melhor vira base; as demais doam trechos).

[2] AVALIAR   → responder por escrito:
                · Que intenção do roteamento ela cobre que hoje está descoberta?
                  (nenhuma → forte candidata a rejeição)
                · Conflita com rules.yaml / RULES.md / qa-protocol?
                · Custo de contexto: tamanho justifica o benefício?
                · Sinais de baixa qualidade: persona inflada, "IA-speak",
                  promessas não verificáveis, instruções vagas

[3] TESTAR    → ciclo skill-testing.md:
                RED   = tarefa-alvo SEM a candidata (baseline do agente)
                GREEN = mesma tarefa COM a candidata
                A candidata só avança se o GREEN mostrar diferença real
                sobre o baseline (não basta "funcionou": tem que melhorar).

[4] REFINAR   → adaptar ao formato STARTER:
                · arquivo `.skill` com cabeçalho padrão (tipo/domínio/idioma)
                · enxugar: cortar persona teatral, manter o que muda resultado
                · idioma conforme language.docs · roteador interno se multi-caso
                · rodapé de autoria do framework + crédito da fonte original

[5] VEREDITO  → ASSIMILAR  → mover para local-skills/ + registrar nos 4 pontos:
                              Start.md (resolução + roteamento) · README.md
                              (tabela) · Start-ops.md (se houver momento claro)
                              → validate-skills.py 0 failed comprova
                ADIAR      → _deferred/ com motivo (potencial real, mas
                              redundante hoje ou dependente de capability futura)
                REJEITAR   → não entra; relatório curto do porquê

[6] LIMPAR    → assimilada: remover o arquivo da pasta de entrada (a versão
                refinada em local-skills/ é a canônica)
                adiada: mover para _deferred/, tirar da pasta de entrada
                rejeitada: renomear REJEITADA_* + motivo em 3–5 linhas no topo
                Registrar lote em skills-governance.md + decisions.yaml
                Fim de lote = atividade pesada → session-review.skill
```

## Regras

- **Proibido assimilar sem GREEN registrado** (P3.1). Log de 1 linha na skill refinada; relatório completo em `skills/outputs/skill-tests/` (local).
- **Proibido assimilar duas skills com a mesma intenção dominante** — consolidar ou escolher uma (lição do P2.8: 9 skills de scroll/fluid viraram 2).
- Candidata que duplica capability ativa **não ganha teste** — rejeição direta na etapa 2 (economiza o custo do subagent), citando a skill existente.
- Lote máximo por sessão: **4 candidatas processadas até veredito** (qualidade > volume).
- O mantenedor pode vetar qualquer veredito — registrar o override em `decisions.yaml`.

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-11
