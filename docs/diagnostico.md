# Diagnóstico — Skills do STARTER

## Resumo executivo

Sim, falta uma skill útil, mas o problema principal hoje não é criar mais uma skill.
O problema principal é que o sistema de roteamento está prometendo skills que não existem no workspace.

## Diagnóstico

A documentação e o roteamento em `skills/governance/Start.md` citam skills como:

- `web-design-cloner`
- `design-taste-frontend`
- `high-end-visual-design`
- `kickoff-doc`
- `designer-research-2627`

Mas, no inventário real de `skills/**/*.skill`, elas não aparecem.

Hoje existe um descompasso entre:

- o que o `STARTER` diz que sabe fazer
- o que ele realmente consegue carregar

Isso é mais grave do que faltar uma skill nova, porque afeta confiança operacional.

## Crítica objetiva

### 1. O gargalo principal não é ausência de capacidade genérica

O sistema já tem capacidade suficiente para:

- kickoff
- prompt estruturado
- design/UI
- QA
- structure por stack

O problema maior está na camada de descoberta e roteamento, que está parcialmente desatualizada.

### 2. Incorporar as boas práticas do artigo não exige, por si só, uma skill nova

Os ajustes propostos antes cabem em governança e templates:

- `kickoff`
- `briefing-template`
- `prompt-engineering`
- `context-scoping`

Ou seja: para incorporar as boas práticas observadas no artigo, não é obrigatório criar uma skill nova.

### 3. Criar uma skill nova agora, antes de corrigir o catálogo, tende a aumentar a bagunça

Antes de expandir o sistema, deveria existir:

- inventário confiável
- roteamento coerente
- `README` sincronizado
- distinção clara entre skill real, skill remota esperada e skill futura

## Falta alguma skill?

Sim. A única lacuna funcional realmente útil é uma skill de direção visual inicial.

### Skill sugerida

`visual-direction-brief.skill`

### Função

Transformar referências visuais vagas em direção visual utilizável, consolidando:

- paleta-base
- tipografia ou tom visual
- densidade
- padrões desejados
- anti-referências

E gerar uma saída curta reutilizável para:

- kickoff
- `PROJECT_BRIEF`
- prompt inicial de UI
- contexto provisório antes do design system formal

## Por que essa skill faz sentido

Hoje o projeto já tem:

- `prompt-engineering.md` para estruturar prompts
- `prompt-library.skill` para prompts prontos
- `interface-design.skill` para UI
- `figma-*` para fluxo com Figma
- `ux-audit.skill` para auditoria

Mas não existe um bloco claramente dedicado a converter referência visual solta em briefing visual objetivo.

Essa lacuna hoje está espalhada entre kickoff, template e prompt engineering, mas não encapsulada como skill.

## Skills que não valem criar agora

Não faz sentido criar neste momento:

- uma skill só para "primeiro prompt"
- uma skill só para "refinamento seguro"
- uma skill só para "anti-meta prompts"

Esses pontos cabem melhor em governança e templates.
Skill deve existir quando há um fluxo reutilizável, não quando há apenas uma regra editorial.

## Ordem recomendada de ação

1. Corrigir o inventário de skills
2. Remover ou marcar como indisponíveis as skills citadas mas ausentes
3. Só depois decidir criar 1 skill nova
4. Se criar, criar `visual-direction-brief.skill`

## Conclusão

Sim, falta uma skill útil de direção visual inicial.
Mas, antes disso, o problema mais importante é sanear o catálogo atual, porque o `STARTER` hoje parece ter skills que, na prática, não estão disponíveis.

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07
