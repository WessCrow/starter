# 📑 Especificação de UX & Conteúdo: STARTER Landing Page

Este documento detalha a estratégia de UX Writing, estrutura de conteúdo e matriz de design da Landing Page oficial do framework **STARTER**, alinhada com as diretrizes do **Designer2627**.

---

## 1. Análise de Contexto & Impacto

*   **Problema de UX:** Desenvolvedores enfrentam alta fricção cognitiva ("paralisia de decisão") ao iniciar novos repositórios: precisam configurar boilerplates, limpar arquivos de templates genéricos e decidir pilhas de tecnologia antes de escrever a primeira linha de código de valor.
*   **Proposta de Valor:** O STARTER inverte esse fluxo: o usuário traz apenas a ideia, o agente faz as perguntas certas e constrói o ambiente perfeito de forma autônoma e segura.
*   **Impacto de Negócio:**
    *   **Redução do TTV (Time-to-Value):** De ~30 minutos de setup manual para < 2 minutos.
    *   **Adoção de Padrões:** Aumento no uso de boas práticas de design e qualidade (QA Gate) logo no Commit #1.

---

## 2. UX Writing & Design de Conteúdo

### Tom e Voz do Framework
*   **Voz (Identidade):** Inteligente, pragmática, orientada a eficiência, minimalista e confiável.
*   **Tom (Contexto):** Inspirador e direto no topo da página (Hero); extremamente prático e didático no passo a passo (Onboarding); técnico e robusto ao falar sobre qualidade (QA Gate).

### Cópia da Landing Page (Estrutura e Seções)

#### A. Hero Section (Seção Principal)
*   **Super-título (Badge):** `Framework STARTER v5.1`
*   **Título Principal:** "Da ideia ao código limpo em 60 segundos."
*   **Subtítulo:** "O ponto de partida inteligente para novos projetos orientados a agentes de IA. Sem configurações manuais, sem boilerplates poluídos, com portaria de qualidade ativa desde o primeiro commit."
*   **CTA Principal (Botão):** `Copiar Starter`
*   **CTA Secundário:** `Como funciona (Vídeo/Docs)`

#### B. Seção de Benefícios (O Contraste)
*   *Título:* "Menos fricção, mais código de verdade."
*   *Tópicos:*
    *   **Adeus Boilerplate Sujo:** O script de cleanup remove resquícios do framework de forma automatizada.
    *   **Entrevista Inteligente:** O agente conduz você com no máximo 4 perguntas em português claro.
    *   **QA Gate:** Toda entrega fecha com build smoke + revisão cética do agente antes de ser marcada como pronta.

#### C. Perfis de Inicialização (A Versatilidade)
*   *Título:* "Pronto para qualquer desafio."
*   *Cartões de Perfil:*
    *   **🌐 Landing Page:** Animações fluidas, SEO estruturado e carregamento ultrarrápido.
    *   **📊 SaaS Dashboard:** Gerenciamento de estado, tabelas dinâmicas e rotas seguras de ponta a ponta.
    *   **⚙️ App Interno:** Telas eficientes de backoffice, CRUDs e tabelas operacionais.
    *   **🎨 Design System:** Tokens semânticos nativos e consistência visual garantida.
    *   **🔌 Backend & API:** Arquitetura limpa, rotas seguras e validações rígidas.

---

## 3. Matriz FEER (Especificação Técnica)

### Tabela de Fluxos (Flows)

| Passo | Ação do Usuário | Resposta do Sistema (Agente) |
| :--- | :--- | :--- |
| **01** | Copia `skills/` e `AGENTS.md` e digita `Começar projeto` | Detecta o comando, roda o cleanup e inicia a interface de entrevista. |
| **02** | Responde às perguntas de escopo (máx. 4) | Consolida as respostas e apresenta o Plano de Implementação (`implementation_plan.md`). |
| **03** | Aprova o plano digitando "Confirmar" | Executa a estrutura, cria os arquivos base e ativa o `qa-gate.skill`. |
| **04** | Roda testes ou implementações adicionais | Executa validações automatizadas e emite o relatório de qualidade. |

### Matriz de Estados de UI (States)

*   **Empty:** Pasta do projeto apenas com `skills/` e `AGENTS.md` (Aguardando ativação).
*   **Loading:** Agente processando respostas da entrevista e gerando a árvore inicial.
*   **Loaded:** Base do projeto gerada, arquivos de configuração carregados com sucesso.
*   **Partial:** Projeto gerado com algumas validações pendentes no QA Gate.
*   **Error:** Falha ao inicializar o framework ou inconformidade detectada pelo validador.
*   **Disabled:** Modo inativo (quando o projeto já foi totalmente iniciado e a skill de setup é congelada para proteção).

---

## 4. Camada Agêntica (Framework IAA)

| Padrão | Texto / Ação de Interface |
| :--- | :--- |
| **Intent Preview** | *"Vou analisar suas respostas para criar uma estrutura modular baseada em Next.js + pnpm com o design system ativo."* |
| **Explainable Rationale** | *"Escolhi pnpm como gerenciador de pacotes padrão devido ao tempo de build 40% menor mapeado na stack."* |
| **Confidence Signal** | *"Alta Confiança: Respostas completas e sem conflitos de dependências."* |
| **Action Audit & Undo** | *Histórico de geração salvo em `skills/core/runtime/decisions.yaml` com a opção de reverter o scaffolding.* |
| **Escalation Pathway** | *"Se o scaffolding gerado não atender ao esperado, digite 'Ajustar plano' para recalibrar o escopo manualmente."* |

---

## 5. Métricas de Sucesso (Framework HEART)

*   **Happiness (Satisfação):** Facilidade percebida pelo desenvolvedor no primeiro uso (NPS pós-setup).
*   **Engagement (Uso):** Frequência de acionamento do comando `Começar projeto` para novas iniciativas.
*   **Adoption (Adoção):** Percentual de novos repositórios criados utilizando a infraestrutura do STARTER.
*   **Retention (Retenção):** Frequência com que o desenvolvedor continua utilizando a pasta de `skills/` para o ciclo contínuo do projeto.
*   **Task Success (Sucesso da Tarefa):** Taxa de kickoffs concluídos com sucesso sem falhas de build inicial.
