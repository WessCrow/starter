# Contrato da sprint — Perfil Starter Lite

> **Data:** 2026-08-21
> **Feature:** 013-starter-lite
> **Perfil desta mudança:** Full — altera a governança do framework
> **Aprovado por você:** [x] Sim — confirmado no chat em 2026-08-21
> **Local:** `specs/013-starter-lite/sprint-contract.md`

---

## Entrega autorizada por este contrato

1. Tornar Lite o perfil padrão dentro da base atual, sem criar outro framework.
2. Permitir que trabalhos pequenos usem somente `spec.md`, com pausa obrigatória para aprovação humana.
3. Promover automaticamente para Full quando algum limite objetivo de risco ou complexidade falhar.
4. Limitar o Gate de Solução aos cinco gatilhos definidos, com no máximo três candidatos do cluster relevante.
5. Corrigir a medição de tokens para contar somente arquivos explicitamente carregados.
6. Registrar Headroom como decisão adiada até existir benchmark real; não integrar a ferramenta nesta sprint.

## Critérios testáveis

| # | Critério | PASS/FAIL |
|---|----------|-----------|
| 1 | `context.yaml` aceita apenas `lite` ou `full`, e o template inicia em `lite`. | PASS |
| 2 | Uma feature Lite aprovada passa com somente `spec.md`; sem aprovação humana, falha. | PASS |
| 3 | Uma feature que viola qualquer limite Lite é roteada para Full antes de implementar. | PASS |
| 4 | O Gate de Solução não busca em pedidos simples e limita uma busca acionada a três candidatos do cluster relevante. | PASS |
| 5 | As fontes solicitadas estão agrupadas e são referências sob demanda, não integrações. | PASS |
| 6 | QA usa `spec.md` como contrato Lite e mantém `sprint-contract.md` para Full. | PASS |
| 7 | A medição recebe paths explícitos e registra somente esses arquivos; path externo ao workspace falha. | PASS |
| 8 | Nenhuma dependência, importação ou serviço Headroom é adicionado. | PASS |
| 9 | Runtime, validação de skills, coerência, testes e higiene retornam sucesso. | PASS |

## Fora desta sprint

- Repositório ou distribuição Lite separado.
- Integração ou benchmark do Headroom.
- Crawler, índice, cache ou ranking automático de fontes externas.
- Mudança nos controles invariantes de segurança, dados e acessibilidade.

## Após implementação

- [x] RED→GREEN registrado para regras/skills alteradas.
- [x] QA Gate executado com relatório cético.
- [x] Estado e handoff apontam para `013-starter-lite`.
- [ ] Usuário faz teste curto com um pedido Lite e outro Full.

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: 2026-08-21
