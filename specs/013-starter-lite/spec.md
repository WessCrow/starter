# spec.md — Perfil Starter Lite

> **Feature:** 013-starter-lite
> **Projeto:** STARTER
> **Criado em:** 2026-08-21
> **Profile:** Full
> **Status:** aprovado
> **Aprovação humana:** sim — 2026-08-21
> **Implementação:** QA PASS — teste humano pendente
> **Protocolo:** `skills/flows/feature-flow.md`

---

## Por quê

O STARTER aplica o mesmo volume de governança a trabalhos de tamanhos diferentes. Isso aumenta documentação, contexto e tempo mesmo quando o pedido é pequeno e de baixo risco. O perfil Lite deve tornar o menor fluxo seguro o padrão, mantendo uma promoção explícita para o fluxo completo quando houver complexidade ou risco verificável.

## Histórias de usuário

| # | Como… | Quero… | Para… | Prioridade |
|---|-------|--------|-------|------------|
| H1 | usuário do STARTER | começar pelo menor fluxo compatível com o pedido | evitar soluções e documentação desproporcionais | alta |
| H2 | mantenedor do STARTER | promover um trabalho Lite para Full quando aparecer risco real | permitir crescimento sem antecipar complexidade | alta |
| H3 | agente executor | verificar soluções existentes somente quando a decisão justificar busca | reutilizar trabalho adequado sem transformar todo pedido em pesquisa | alta |
| H4 | mantenedor do STARTER | avaliar compressão de contexto com evidência comparável | decidir sobre Headroom sem integração prematura | média |

## Critérios de aceite (testáveis)

1. Antes de executar um pedido, o STARTER classifica silenciosamente a menor solução suficiente entre não fazer, reutilizar, configurar, código mínimo e sistema; uma solução maior só é escolhida quando a anterior falha em critério verificável.
2. Um trabalho classificado como pequeno usa somente `spec.md` como documentação da feature e não exige `plan.md`, `tasks.md` ou `sprint-contract.md`.
3. O fluxo promove Lite para Full antes da implementação quando houver mudança arquitetural, nova integração ou dependência, risco relevante de segurança ou perda de dados, escopo incerto, ou quando o trabalho deixar de cumprir os limites objetivos do Lite.
4. O Gate de Solução só dispara para nova dependência, componente, integração, ferramenta ou decisão arquitetural; consulta primeiro recursos já conectados ou instalados e depois, se necessário, no máximo três alternativas externas do cluster relevante.
5. Cada alternativa externa informa adequação ao problema, custo de adoção, manutenção, licença e motivo de aceitar ou descartar; uma lista fixa de sites funciona como fonte de busca, não como integração obrigatória.
6. Headroom não é dependência do perfil Lite. Sua adoção futura depende de benchmark isolado que compare tokens de entrada e saída, latência, qualidade e taxa de falha contra uma linha de base sem compressão.
7. A medição de contexto do STARTER representa apenas os arquivos efetivamente carregados para a tarefa, sem somar automaticamente todo o catálogo e todos os fluxos.
8. Regras de segurança, prevenção de perda de dados, acessibilidade, evidência antes de conclusão e QA aplicável permanecem obrigatórias nos perfis Lite e Full.
9. O perfil Full atual continua disponível, e um trabalho promovido mantém o `spec.md` já criado como origem do fluxo completo.

## Análise de Riscos

- **Risco:** o Lite virar uma forma de pular segurança ou validação.
  - **Mitigação:** manter invariantes não dispensáveis e promover automaticamente trabalhos com risco relevante.
- **Risco:** critérios vagos fazerem cada agente classificar o mesmo pedido de forma diferente.
  - **Mitigação:** usar condições objetivas, casos de fronteira testados e decisão registrada no próprio `spec.md`.
- **Risco:** o Gate de Solução adicionar pesquisa e latência a ajustes simples.
  - **Mitigação:** acioná-lo somente nas cinco categorias declaradas e limitar a busca externa a três alternativas.
- **Risco:** manter dois frameworks divergentes.
  - **Mitigação:** implementar Lite como perfil da base atual, sem distribuição ou árvore paralela mantida manualmente.
- **Risco:** compressão remover informação necessária e degradar a resposta.
  - **Mitigação:** não integrar Headroom nesta entrega; exigir benchmark com qualidade e falhas, além de economia de tokens.
- **Risco:** a própria governança Lite aumentar o contexto global.
  - **Mitigação:** alterar o mínimo de regras existentes e carregar detalhes somente quando o perfil ou o gate forem acionados.

## Fora do escopo

- Criar um repositório ou distribuição Starter Lite separado.
- Integrar Headroom ao runtime nesta entrega.
- Criar buscador, crawler, catálogo sincronizado ou ranking automático de projetos externos.
- Garantir que uma alternativa externa exista para todo pedido.
- Remover os controles invariantes de segurança, acessibilidade e prevenção de perda de dados.

## Clarificações

| Data | Pergunta | Resposta |
|------|----------|----------|
| 2026-08-21 | No Lite, o pedido original já autoriza implementar após registrar `spec.md`, ou ainda deve haver uma pausa para aprovação explícita do spec? | Sempre pausar e pedir aprovação explícita ao humano antes de implementar. |

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: 2026-08-21
