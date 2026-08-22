# plan.md — Perfil Starter Lite

> **Feature:** 013-starter-lite
> **Baseado em:** `spec.md` (status: clarificado)
> **Criado em:** 2026-08-21
> **Protocolo:** `skills/flows/feature-flow.md`

---

## Stack e dependências

- Stack do projeto: documentação Markdown/YAML e scripts Python 3 existentes.
- Novas dependências: nenhuma. Usar somente biblioteca padrão e dependências já presentes no runtime.

## Modelo de dados

O runtime passa a aceitar um campo de governança no contexto:

```yaml
governance:
  profile: lite # lite | full
```

O `spec.md` de cada feature declara o perfil aplicado e o estado de aprovação humana. No perfil Lite, esse documento também é a fonte dos critérios usada pelo QA.

## Arquitetura da feature

```text
context.yaml
  └── governance.profile = lite | full
          ↓
action-router + feature-flow
  ├── Lite: spec → aprovação humana → implementação → QA
  └── Full: spec → plan → tasks → contrato → aprovação → implementação → QA

priority-matrix.skill
  └── Gate de Solução acionado → solution-sources.yaml (somente cluster relevante)

check-spec-coherence.py + independent-qa.py
  ├── Lite: validam spec aprovado
  └── Full: validam spec + plan + tasks + contrato

calculate_tokens.py
  └── recebe lista explícita dos arquivos efetivamente carregados
```

Arquivos novos:

- `skills/catalog/solution-sources.yaml`: fontes agrupadas, carregadas somente quando o Gate de Solução disparar.
- `skills/infra/tests/test_calculate_tokens.py`: regressão da medição explícita.

Arquivos alterados:

- `AGENTS.md`
- `skills/core/runtime/context.yaml`
- `skills/core/runtime/schema/context.schema.json`
- `skills/core/runtime/routes.yaml`
- `skills/core/runtime/qa.yaml`
- `skills/core/runtime/schema/qa.schema.json`
- `skills/templates/runtime/context.yaml`
- `skills/templates/runtime/schema/context.schema.json`
- `skills/templates/runtime/routes.yaml`
- `skills/templates/runtime/qa.yaml`
- `skills/templates/runtime/schema/qa.schema.json`
- `skills/templates/specs/spec-template.md`
- `skills/flows/feature-flow.md`
- `skills/flows/action-router.md`
- `skills/catalog/action-router.skill`
- `skills/catalog/priority-matrix.skill`
- `skills/catalog/qa-gate.skill`
- `skills/catalog/qa-playwright.skill`
- `skills/flows/qa-protocol.md`
- `skills/infra/scripts/check-spec-coherence.py`
- `skills/infra/scripts/independent-qa.py`
- `skills/infra/tests/test_spec_coherence.py`
- `skills/infra/tests/test_independent_qa.py`
- `skills/scripts/calculate_tokens.py`
- `skills/core/runtime/decisions.yaml`
- arquivos de estado e handoff do runtime.

## Rotas e contratos

| Entrada | Condição | Saída |
|---------|----------|-------|
| Pedido novo | Todos os limites Lite passam | Criar somente `spec.md`, parar e pedir aprovação humana |
| Pedido novo | Qualquer limite Lite falha | Promover para Full antes de implementar |
| Decisão de solução | É dependência, componente, integração, ferramenta ou arquitetura | Consultar o cluster relevante e apresentar no máximo três candidatos |
| Medição de contexto | Lista explícita de paths carregados | Atualizar `handoff.context_metrics` apenas com esses arquivos |
| Avaliação de Headroom | Benchmark futuro aprovado | Comparar controle e tratamento; não integrar automaticamente |

## Limites objetivos do Lite

Lite somente quando **todos** forem verdadeiros:

1. Um comportamento ou entregável pequeno e claramente definido.
2. No máximo três critérios de aceite.
3. Estimativa de até três arquivos de implementação alterados.
4. Sem nova dependência, integração externa, entidade, rota, tabela, migração ou camada arquitetural.
5. Sem autenticação, autorização, pagamentos, dados sensíveis, operação destrutiva ou risco relevante de perda de dados.
6. Mudança reversível sem migração.
7. O humano aprovou explicitamente o `spec.md`.

Qualquer falha promove o trabalho para Full. A promoção reaproveita o mesmo `spec.md`.

## Nível arquitetural e matriz de prioridade

- **Nível arquitetural:** L — mudança transversal no runtime, roteamento, QA e medição; não cria subsistema independente.
- **Matriz:** N2 para compor e configurar mecanismos existentes; N3 apenas nos dois pontos em que configuração não garante comportamento determinístico: coerência de specs e medição de tokens.
- **Frase-teste:** escolhi N2 porque N1 já oferece action router, matriz, validador e QA, mas eles falham em aceitar `spec.md` como contrato Lite e em medir somente o contexto carregado. Escolhi N3 nesses validadores porque N2 não consegue verificar essas condições mecanicamente.
- **Descartado:** Starter Lite separado — duplicaria manutenção e criaria divergência.
- **Descartado:** integração Headroom — não existe benchmark local que demonstre ganho líquido de tokens, qualidade e latência.
- **Descartado:** buscador/crawler próprio — a consulta sob demanda já atende o Gate de Solução.
- **Descartado:** DDD, event sourcing e arquitetura hexagonal — não existe domínio, auditoria temporal ou integração que justifique essas camadas.

## Gate de Solução

| Problema | Recurso existente escolhido | Alternativa descartada | Motivo |
|----------|-----------------------------|------------------------|--------|
| Classificar proporcionalidade | `priority-matrix.skill` | novo motor de decisão | a matriz já implementa N0–N4 |
| Rotear Lite/Full | `action-router` + `feature-flow` | novo starter | evita duas bases |
| Validar specs | `check-spec-coherence.py` | novo validador | extensão pequena e testável |
| QA Lite | `qa-gate.skill` + `independent-qa.py` | pipeline paralelo | mantém uma portaria de qualidade |
| Fontes externas | arquivo de dados carregado sob demanda | APIs/crawler | fontes mudam e não exigem integração |
| Economia de contexto | corrigir `calculate_tokens.py` | Headroom agora | primeiro é necessário medir corretamente |

Clusters previstos na fonte sob demanda: código/projetos; componentes/design systems; UI/prompts; geração visual; navegação de código; contexto/tokens; frameworks de agentes. Adoção exige licença e adequação verificadas; licença permissiva não implica adoção automática.

## Riscos e decisões

| Decisão | Rastreia para | Alternativa descartada | Motivo |
|---------|---------------|------------------------|--------|
| Lite é o perfil padrão | Critérios 1, 2 e 9 | Full padrão | antecipa documentação sem evidência de necessidade |
| Aprovação humana é obrigatória no Lite | Critérios 2 e 8 | autorização implícita | usuário exigiu controle antes da execução |
| Promoção é conservadora e automática | Critérios 3 e 8 | Lite por preferência | risco não pode ser rebaixado por conveniência |
| Gate usa no máximo três opções do cluster relevante | Critérios 4 e 5 | varredura universal | reduz latência e ruído |
| Headroom fica adiado | Critério 6 | integração imediata | falta linha de base local |
| Medição exige paths explícitos | Critério 7 | contar todo o framework | a soma atual não representa contexto real |

## Benchmark futuro do Headroom

Não será implementado nesta sprint. Uma avaliação futura deverá usar tarefas reais e comparar controle sem compressão contra tratamento com Headroom, registrando: tokens de entrada, tokens de saída, latência p50/p95, critérios de qualidade aprovados e falhas. Sem redução relevante e repetível, sem regressão material de qualidade e sem custo operacional aceitável, a decisão padrão será não adotar.

## Constitution check

- [x] Nenhuma regra de segurança, perda de dados ou acessibilidade é removida.
- [x] Nenhuma dependência ou serviço externo é integrado.
- [x] A solução reutiliza runtime, roteamento, QA e validadores existentes.
- [x] O Gate de Solução é condicional; não adiciona busca a pedidos simples.
- [x] O humano continua aprovando antes de qualquer implementação Lite ou Full.

## Analyze — 2026-08-21

- [x] Os nove critérios de aceite rastreiam para tarefas verificáveis.
- [x] Nenhuma tarefa ficou sem requisito; itens de implementação são necessários para manter runtime, templates e QA coerentes.
- [x] Spec, plan, tasks, `rules.yaml` e `AGENTS.md` não apresentam contradição.
- [x] Não existem marcações `[PRECISA CLARIFICAR]` pendentes.
- [x] Tipos de domínio não se aplicam; o único contrato de dados é validado por JSON Schema.
- [x] O nível L é proporcional à mudança transversal; não foi proposta camada ou serviço novo.
- [x] Gate de Solução cumprido com reutilização dos mecanismos locais e descarte de Starter separado, crawler e Headroom imediato.
- [x] Evidência: `check-spec-coherence.py --strict` → 30 checks, 0 falhas; `validate.py` → 11 passed, 0 failed; `validate-skills.py` → 53 passed, 0 failed; `git diff --check` sem erros.

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: 2026-08-21
