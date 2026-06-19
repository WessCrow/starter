# spec.md — Refatoração de Robustez e Automação de DX (Boris Cherny Style)

> **Feature:** 009-refatoracao-boris
> **Projeto:** STARTER
> **Criado em:** 2026-06-19
> **Status:** rascunho
> **Protocolo:** `skills/flows/feature-flow.md`

---

## Por quê

O STARTER possui uma estrutura robusta de governança, mas ela é fortemente baseada em documentação manual e estimativas estáticas em Markdown/YAML realizadas pelo próprio agente (ex: specs, plans, contagem de tokens manual). Para torná-lo um ecossistema produtivo e escalável, é necessário:
1. Substituir a documentação manual de escopo técnico por especificações escritas diretamente em código (garantias em tempo de compilação).
2. Automatizar processos repetitivos da IA (como o cálculo de tokens da janela de contexto).
3. Reduzir a barreira de burocracia para pequenas alterações estéticas ou correções de bugs, permitindo um pipeline desobstruído para micro-tarefas.
4. Garantir robustez em runtime forçando o mapeamento completo e explícito dos caminhos de erro nas interfaces do usuário.

---

## Histórias de usuário

| # | Como… | Quero… | Para… | Prioridade |
|---|-------|--------|-------|------------|
| **H1** | Desenvolvedor Humano | Iniciar o planejamento de features especificando contratos e estruturas de tipos do código | Que o compilador TypeScript atue como o primeiro auditor de consistência lógica, eliminando a ambiguidade de especificações textuais extensas. | Alta |
| **2** | Arquiteto / Mantenedor | Bloquear automaticamente qualquer entrega que possua tipos inseguros ou código sem tratativas assíncronas adequadas | Garantir que o código gerado pelo agente mantenha padrões estritos de qualidade sênior, sem atalhos que causem bugs em produção. | Alta |
| **3** | Agente de IA / Sistema | Ter os metadados de tokens calculados automaticamente na auditoria de contexto | Reduzir o desperdício de tokens de saída da IA e eliminar erros matemáticos durante a etapa de handoff de contexto. | Média |
| **4** | Desenvolvedor Humano | Aplicar pequenos ajustes visuais ou de código sem precisar passar pela esteira completa de specs | Agilizar a DX do dia a dia, mantendo o processo fluido para correções que não alteram estados ou entidades principais. | Alta |
| **5** | Engenheiro de Software | Garantir que todas as falhas de componentes ou APIs do domínio sejam tratadas explicitamente via tipos | Evitar que exceções silenciosas de runtime quebrem a aplicação, forçando a representação de falhas diretamente nas assinaturas do código. | Alta |

---

## Critérios de aceite (testáveis)

1. **Type-First Specs:** O fluxo de especificação de novas features do STARTER deve guiar o agente a iniciar a modelagem por contratos de tipo antes de detalhar a implementação.
2. **Compiler & Lint Gates:** O pipeline de teste de fumaça (`qa-smoke`) deve reprovar commits ou tarefas que utilizem tipos flexíveis (`any`), type casting inadequados ou que tenham erros de lint assíncronos.
3. **Cálculo de Tokens Automatizado:** O arquivo de handoff de contexto deve ter seu tamanho de tokens populado dinamicamente por um script executado nos bastidores, não por estimativa da IA.
4. **Fast-Track de Ajuste Trivial:** O agente deve ter suporte nativo a um comando rápido de ajuste que ignora a criação de arquivos de especificação (pula a burocracia) quando o escopo atender a critérios rígidos.
5. **Tratamento de Exceções Funcional:** O repositório deve fornecer templates onde tratamentos de erro são definidos como tipos de união fechados em vez de capturas genéricas de exceções.

---

## Fora do escopo

* Criar uma biblioteca externa independente do STARTER para tratamento funcional de erros (devemos usar os próprios padrões do TypeScript/Zod).
* Automatizar os builds ou CI de ambientes externos de nuvem (ex: AWS, Vercel). O foco é o pipeline local de DX e Git.

---

## Clarificações

> Preenchido na fase Clarify (`feature-flow.md` fase 2). Não apagar respostas.

| Data | Pergunta | Resposta |
|------|----------|----------|
| 2026-06-19 | [PRECISA CLARIFICAR: O script de cálculo de tokens deve ser escrito em que linguagem para garantir portabilidade entre os projetos consumidores do STARTER?] | |
| 2026-06-19 | [PRECISA CLARIFICAR: Como faremos para configurar o Husky e o lint-staged de forma opcional nos projetos que não possuam Git inicializado ou usem outro gerenciador de tarefas?] | |

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: 2026-06-19
