<!-- lp-github.md = espelho do README.md (fonte). Ajuste apenas os caminhos relativos. -->

# STARTER

> **A governança que começa pequena — e só cresce quando o risco exige.**

[![Runtime](https://img.shields.io/badge/Runtime-v5.5-8B5CF6?style=flat-square&logo=yaml&logoColor=white)](../../skills/core/runtime/index.yaml)
[![Starter Lite](https://img.shields.io/badge/Starter-Lite_por_padrão-2563EB?style=flat-square)](../../specs/013-starter-lite/spec.md)
[![QA Gate](https://img.shields.io/badge/QA_Gate-Ativo-10B981?style=flat-square&logo=github-actions&logoColor=white)](../../skills/catalog/qa-smoke.skill)
[![License MIT](https://img.shields.io/badge/License-MIT-F59E0B?style=flat-square)](../../LICENSE)

O STARTER é uma camada local de governança para agentes de IA que constroem software. Ele reduz o processo quando o pedido é pequeno, promove o trabalho para um fluxo completo quando aparece risco real e mantém aprovação humana, segurança e QA em qualquer tamanho de entrega.

[**Começar em 3 passos**](#comece-em-3-passos) · [Entender Lite → Full](#lite-por-padrão-full-quando-necessário)

---

## O problema não é falta de velocidade. É falta de proporção.

Sem regras claras, um agente pode transformar um ajuste pequeno em arquitetura desnecessária — ou tratar uma mudança arriscada como se fosse simples. Nos dois casos, você perde controle: por excesso de processo ou por falta de proteção.

O STARTER dá uma régua objetiva ao agente:

- começar pela menor solução que resolve o problema;
- pedir aprovação antes de implementar uma feature;
- aumentar o rigor somente quando escopo, dependência ou risco exigirem;
- apresentar evidência antes de dizer que algo funciona.

## Lite por padrão, Full quando necessário

O STARTER não é dividido em dois produtos. Existe uma única base, com dois níveis de governança.

| | **Lite** | **Full** |
|---|---|---|
| Quando usar | Entrega pequena, clara e reversível | Escopo maior, incerto ou com risco relevante |
| Documentação | Apenas `spec.md` | `spec.md`, plano, tarefas e contrato de sprint |
| Limites | Até 3 critérios e 3 arquivos de implementação | Ativado quando qualquer limite Lite falha |
| Dependências e integrações | Nenhuma nova | Avaliadas e registradas antes da implementação |
| Aprovação humana | Obrigatória | Obrigatória |
| QA | Obrigatório | Obrigatório |

Uma feature é promovida para Full antes do código quando envolve nova dependência ou integração, mudança arquitetural, autenticação, pagamentos, dados sensíveis, risco de perda de dados ou escopo que deixou de ser pequeno e definido.

> **Lite não significa “sem processo”.** Significa usar apenas o processo necessário, sem remover as proteções que evitam retrabalho e dano.

## Como o STARTER trabalha

```text
Pedido
  ↓
Menor solução suficiente (N0 → N4)
  ↓
Spec curta e aprovação humana
  ↓
Lite permanece pequeno ── ou ── risco promove para Full
  ↓
Implementação
  ↓
QA Gate + evidência
```

O agente lê regras e estado diretamente do projeto. Isso mantém as decisões entre sessões e IDEs sem depender da memória do chat.

## O que continua obrigatório

O perfil muda o volume de governança, não o padrão de segurança.

| Garantia | Como o STARTER aplica |
|---|---|
| Você continua no controle | Nenhuma feature é implementada antes da aprovação explícita |
| Solução proporcional | A matriz N0–N4 força o agente a justificar cada aumento de complexidade |
| Host protegido | O Host Guard bloqueia comandos destrutivos e ações fora do projeto |
| Entrega verificável | O QA Gate exige validação; na Fase 4, features com UI também passam pelo Playwright |
| Contexto recuperável | Estado e handoff em YAML preservam decisões entre sessões e IDEs |
| UI com referência | O Gate de Fidelidade impede inventar uma interface quando existe Figma |

## Para quem faz sentido

- Pessoas que constroem software com Cursor, Claude Code, Antigravity, VSCode, Windsurf, Cline ou Roo.
- Times que querem autonomia do agente sem abrir mão de aprovação e rastreabilidade.
- Projetos que sofrem tanto com over-engineering quanto com mudanças rápidas sem validação.
- Mantenedores que preferem regras versionadas no repositório a instruções perdidas no histórico do chat.

## O que o STARTER não é

- Não é um template visual nem um boilerplate preso a uma stack.
- Não substitui revisão humana em decisões críticas.
- Não promete eliminar toda falha de IA.
- Não cria documentação pesada para toda mudança: trabalhos pequenos permanecem pequenos.

## Comece em 3 passos

1. Copie [AGENTS.md](../../AGENTS.md) e a pasta [skills/](../../skills) para a raiz do seu projeto.
2. No chat do seu editor, digite **`Começar projeto`**.
3. Responda até quatro perguntas, revise o resumo e confirme quando estiver de acordo.

O agente prepara o contexto do projeto e passa a aplicar o fluxo Lite/Full automaticamente. Para uma visão rápida do primeiro uso, consulte [COMECAR-PROJETO.md](../../COMECAR-PROJETO.md).

## Compatibilidade

| Ambiente | Como funciona |
|---|---|
| Cursor, Claude Code e Antigravity | Leitura nativa das regras do projeto |
| VSCode, Windsurf, Cline e Roo | Compatível por `AGENTS.md` |
| macOS, Linux e Windows | Scripts shell no Windows exigem WSL ou Git Bash |

Recursos opcionais, como hooks e orquestração por tier, degradam para convenções manuais quando o editor não oferece suporte. O fluxo principal continua utilizável.

## Open source, com licença clara

O STARTER é distribuído sob a [Licença MIT](../../LICENSE). Você pode usar, copiar, modificar e distribuir o projeto, preservando o aviso de copyright e os termos da licença.

Mantido por **Wesley Alves**.

[Portfólio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
