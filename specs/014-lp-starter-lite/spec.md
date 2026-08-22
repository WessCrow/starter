# spec.md — Landing page da proposta Starter Lite

> **Feature:** 014-lp-starter-lite
> **Projeto:** STARTER
> **Criado em:** 2026-08-21
> **Profile:** Lite
> **Status:** aprovado
> **Aprovação humana:** sim — 2026-08-21
> **Implementação:** QA PASS — revisão humana pendente
> **Protocolo:** `skills/flows/feature-flow.md`

---

## Por quê

A apresentação pública atual descreve principalmente a estrutura técnica do STARTER e ainda não comunica a nova proposta: começar com o menor fluxo seguro, usar Lite por padrão e promover para Full somente quando complexidade ou risco justificarem. A landing page deve ajudar quem usa agentes de IA a entender rapidamente o problema, o diferencial, as garantias mantidas e como experimentar o framework. O repositório também precisa declarar de forma inequívoca os termos de uso e distribuição por meio da licença MIT.

## Histórias de usuário

| # | Como… | Quero… | Para… | Prioridade |
|---|-------|--------|-------|------------|
| H1 | pessoa que usa agentes de IA para criar software | entender em poucos minutos a proposta Lite/Full | decidir se o STARTER resolve excesso de processo sem abrir mão de segurança | alta |
| H2 | pessoa interessada em experimentar o STARTER | encontrar um caminho de adoção curto e claro | começar sem precisar dominar a estrutura interna do framework | alta |
| H3 | pessoa que reutiliza ou contribui com o projeto | saber sob quais termos o código pode ser usado | copiar, modificar e distribuir o projeto com segurança jurídica | alta |

## Critérios de aceite (testáveis)

1. A apresentação pública explica com linguagem direta: o problema do excesso de governança, o Lite como menor fluxo seguro, a promoção objetiva para Full e as garantias que nunca são removidas, sem promessas genéricas ou contradições com o comportamento real do STARTER.
2. A página conduz o leitor por uma narrativa de conversão completa — proposta principal, para quem é, como funciona, benefícios verificáveis, limites honestos, início em três passos e uma chamada principal para experimentar — e as duas versões públicas do conteúdo permanecem equivalentes.
3. O repositório contém a licença MIT padrão, com `Copyright 2026 Wesley Alves`; a apresentação identifica o projeto como open source sob MIT e oferece acesso claro aos termos, sem alterar nem resumir o texto jurídico da licença.

## Análise de Riscos

- **Risco:** a nova copy prometer simplicidade absoluta e esconder os gates obrigatórios.
  - **Mitigação:** apresentar Lite como fluxo menor, não como ausência de aprovação, segurança ou QA; explicar quando ocorre a promoção para Full.
- **Risco:** a página ficar persuasiva, mas incompatível com a implementação atual.
  - **Mitigação:** usar apenas mecanismos já entregues e validados na feature 013; evitar métricas, depoimentos e resultados não comprovados.
- **Risco:** a licença ou a atribuição ficarem inconsistentes entre os pontos públicos.
  - **Mitigação:** usar integralmente o texto MIT aprovado pela OSI, identificar o titular e manter um único arquivo jurídico como fonte dos termos.

## Fora do escopo

- Criar um site novo, rota web, identidade visual, imagens ou animações.
- Adicionar telemetria, formulário, captura de leads ou integração externa.
- Alterar os fluxos Lite/Full, os gates de segurança ou a implementação da feature 013.
- Inventar métricas de adoção, prova social ou comparações não verificadas.

## Clarificações

| Data | Pergunta | Resposta |
|------|----------|----------|
| 2026-08-21 | O que significa “proposta nova” neste pedido? | O contexto ativo define a proposta como Starter Lite por padrão, com promoção objetiva para Full e invariantes de segurança e QA. |
| 2026-08-21 | A landing page será um site novo ou a apresentação pública já existente? | O repositório já usa o README como fonte e `docs/public/lp-github.md` como espelho; a solução mínima é refazer esse conteúdo existente. |
| 2026-08-21 | Qual titular deve constar na licença? | A autoria e a manutenção registradas no projeto identificam Wesley Alves; será usado `Copyright 2026 Wesley Alves`. |

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: 2026-08-21
