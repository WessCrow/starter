# O que é o STARTER

## Definição curta

O `STARTER` é um framework operacional para iniciar, estruturar, evoluir e validar projetos com agentes de IA.

Ele não entrega só uma base de código.  
Ele entrega um fluxo de trabalho com:

- kickoff guiado
- memória operacional para IA
- roteamento de skills por intenção
- estrutura inicial por stack
- QA gate obrigatório

---

## O que ele é

O `STARTER` é:

- um **sistema de kickoff** para tirar um projeto do zero com poucas perguntas
- um **runtime AI-native** com contexto persistente em `skills/runtime/*.yaml`
- um **orchestrator de skills** para escolher a capacidade certa conforme a tarefa
- um **framework de governança** para reduzir deriva entre sessões
- um **guardrail de qualidade** para impedir que implementação seja dada como pronta sem validação

Em termos práticos, ele serve para transformar:

```txt
ideia solta → perguntas certas → estrutura inicial → contexto persistente → execução → QA
```

---

## O que ele não é

O `STARTER` não é:

- um boilerplate frontend comum
- um template visual pronto
- um gerador mágico de app em uma única rodada
- uma coleção solta de prompts
- um substituto para repertório técnico, produto ou direção visual

Ele organiza e melhora o processo com IA.  
Ele não elimina a necessidade de critério.

---

## Para que ele serve

O `STARTER` serve para:

- começar projetos novos sem caos inicial
- manter consistência entre sessões com agentes
- estruturar apps com base em stack e escopo
- documentar decisões sem depender só da memória da conversa
- impor um fluxo mínimo de contrato, implementação e QA
- apoiar projetos com exigência de UI, consistência e craft visual

---

## Problemas que ele resolve

Sem o `STARTER`, é comum acontecer:

- cada sessão de IA recomeça do zero
- o projeto nasce sem estrutura clara
- docs e código se contradizem
- a IA improvisa demais
- a qualidade final depende só de memória de chat
- features são dadas como prontas sem gate real

O `STARTER` existe para reduzir exatamente isso.

---

## Como ele opera

Os blocos principais do sistema são:

1. **Kickoff**
   O usuário diz `Começar projeto`, responde poucas perguntas e confirma o resumo.

2. **Structure**
   O sistema detecta a stack e cria a base correta do projeto.

3. **Runtime**
   O contexto operacional da IA vive em YAML, separado da documentação humana.

4. **Skills**
   O agente escolhe habilidades específicas conforme a intenção da tarefa.

5. **QA Gate**
   Nada relevante deveria ser marcado como concluído sem validação.

---

## Onde ele é mais forte

Hoje o `STARTER` é especialmente forte em:

- kickoff orientado
- memória operacional para agentes
- governança de execução
- consistência entre docs, skills e roteamento
- projetos com UI e direção visual relevante

---

## Onde ele não deve ser vendido errado

Não faz sentido vender o `STARTER` como:

- “tema pronto”
- “kit de componentes”
- “framework só de design”
- “fábrica automática de SaaS”

O valor real dele está na combinação de:

- processo
- contexto
- consistência
- validação

---

## Custo de contexto por sessão

O STARTER não é invisível em tokens — e esse número é medido, não estimado.

**Metodologia:** `validate-skills.py` mede o tamanho em bytes de cada camada de contexto definida em `skills/runtime/context-budget.yaml`. Conversão: 1 token ≈ 4 bytes (GPT-tokenizer para texto em inglês/PT-BR técnico).

| Camada | Conteúdo | Tamanho | Tokens est. |
|--------|----------|---------|-------------|
| **hot** (sempre carregada) | AGENTS.md, INDEX, state, handoff, qa.yaml | 15.401 bytes | ~3.850 |
| **warm** (sob demanda frequente) | skills de governance ativas da sessão | 4.107 bytes | ~1.030 |
| **entrada** (docs de orientação) | COMECAR-PROJETO + Start.md | 8.474 bytes | ~2.120 |
| **Sessão típica (hot + warm + entrada)** | — | **27.982 bytes** | **~7.000** |

Referência: um modelo com janela de 200 k tokens comporta ~28 sessões STARTER completas em paralelo. Em uso real, apenas hot (~3.850 tok) é carregada em toda sessão; warm e entrada entram sob demanda.

Medição registrada em: 2026-06-12 · versão do framework: v5.2 · fonte: `skills/runtime/context-budget.yaml`.

---

## Descrição de posicionamento

O `STARTER` é um framework AI-native para começar projetos com agentes sem perder contexto, consistência e qualidade.  
Ele combina kickoff guiado, memória operacional, roteamento de skills, estrutura por stack e QA gate para transformar uma ideia em um projeto evoluível, em vez de apenas gerar arquivos iniciais.

---

## Resumo final

Se eu tivesse que resumir em uma frase:

> O `STARTER` não serve só para criar projeto.  
> Ele serve para **começar certo e continuar com consistência usando IA**.

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-12
