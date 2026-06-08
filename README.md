# 🚀 STARTER

<p align="center">
  <strong>O ponto de partida inteligente para novos projetos orientados a agentes de IA.</strong><br>
  Uma estrutura leve, autogerenciada e focada em eliminar a fricção inicial do desenvolvimento.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Runtime-v5.1_Enterprise-blueviolet?style=for-the-badge" alt="Runtime v5.1">
  <img src="https://img.shields.io/badge/QA_Gate-Strict-emerald?style=for-the-badge" alt="QA Gate Strict">
  <img src="https://img.shields.io/badge/UX_Standard-Designer2627-ff69b4?style=for-the-badge" alt="UX Standard Designer2627">
</p>

---

## ⚡ A Promessa
**Você entra com uma ideia crua. O agente conduz o desenvolvimento guiado e entrega estrutura limpa, código pronto e economia de custos.**

Esqueça o tempo gasto configurando ambientes, limpando templates pesados ou decidindo arquiteturas sozinho. Com o **STARTER**, um assistente de desenvolvimento guiado conduz você por uma entrevista curta de até 4 perguntas simples e gera um setup sob medida, utilizando uma arquitetura modular de contexto que economiza tokens e mantém a execução focada.

---

## 🎯 Como Funciona em 60 Segundos

Apenas 2 arquivos de infraestrutura inicial e 1 comando no chat.

```mermaid
graph TD
    A[Sua Ideia Crua] --> B[Copiar skills/ & AGENTS.md]
    B --> C[Digitar: 'Começar projeto']
    C --> D[Entrevista de IA: Max 4 perguntas]
    D --> E[Aprovação do Plano]
    E --> F[Geração da Base + QA Gate Ativo]
```

### O Caminho Principal:
1. Crie ou abra a pasta vazia do seu novo projeto.
2. Copie a pasta `skills/` e o arquivo `AGENTS.md` para dentro dela.
3. No chat do seu editor favorito (Cursor, Claude Code, Antigravity, etc.), digite:
   ```bash
   Começar projeto
   ```
4. Responda às perguntas simples do agente, revise o plano gerado e confirme!

## ✨ O que você ganha vs. O que o STARTER evita

| 🎁 O que você ganha | 🚫 O que você nunca mais faz |
| :--- | :--- |
| **Assistente de desenvolvimento guiado** via chat interativo | ❌ Escrever documentações extensas e PRDs do zero |
| **Sincronização Multi-IDE Sem Quebras** (Cursor, Antigravity, Cline, etc.) | ❌ Perder histórico ou desconfigurar o projeto ao trocar de editor |
| **Até 80% de economia de tokens** com contexto Hot/Warm/Cold e Context Cleaner | ❌ Estourar limite de contexto de IA com arquivos redundantes |
| **Host Guard Integrado:** Isolamento local contra comandos perigosos e vazamentos | ❌ Executar scripts acidentais ou expor credenciais `.env` no Git |
| **Parceiro de Engenharia Full-Stack:** Diretrizes claras de Front, Back e SOLID | ❌ Hardcodar estilos, gerar re-renders desnecessários ou violar acoplamento |
| **QA Gate integrado** (Validação automática de build/lint obrigatória) | ❌ Subir código quebrado ou sem testes básicos |

---

## 🗺️ Escolha seu Ponto de Partida

Durante o onboarding interativo, você pode guiar o agente para gerar qualquer um dos perfis abaixo:

*   **🌐 Landing Page (LP)**  
    *Foco:* Páginas de produto, conversão rápida e estética premium com animações fluidas e tokens de design CSS.
*   **📊 SaaS Dashboard**  
    *Foco:* Área logada, visualização de métricas, tabelas dinâmicas, gerenciamento previsível de estado (Zustand) e rotas seguras.
*   **⚙️ App Interno (Backoffice)**  
    *Foco:* Painéis operacionais rápidos, CRUDs automatizados, facilidade de uso e layout eficiente.
*   **🎨 Design System**  
    *Foco:* Tokens de design semânticos, consistência de marca, componentes reutilizáveis e acessibilidade nativa (WCAG POUR).
*   **🔌 Backend & API**  
    *Foco:* Serviços robustos, validação estrita na borda com Zod, tratamento limpo de erros e segurança de variáveis.

---

## 🛠️ Sob o Capô: O Runtime OS v5.1

O STARTER funciona como um sistema operacional conversacional de desenvolvimento. Ele se autogerencia através de uma arquitetura baseada em estados:

1. **`runtime/index.yaml`**: Ordem de inicialização e dependências ativas.
2. **`runtime/rules.yaml` & `runtime/context.yaml`**: Contexto quente com regras do Host Guard, Front, Back e diretrizes de Arquitetura.
3. **`validate.py`**: O guardião de integridade que valida schemas YAML e audita o workspace contra vazamentos de credenciais locais.
4. **`context-cleaner.skill`**: O auditor local que ajuda a organizar os arquivos de contexto e reduzir o desperdício de tokens.
5. **`QA Gate (qa-gate.skill)`**: A revisão obrigatória pós-implementação que garante a corretude funcional antes de liberar o código.

---

## 💻 Compatibilidade e Ecossistema

*   **Experiência Premium:** Cursor, Claude Code e Antigravity (leitura nativa de `AGENTS.md` e execução rápida).
*   **Compatível:** VSCode, Windsurf, Cline, Roo.
*   **Padrão de Stack:** Next.js + pnpm (ou React + Vite para SPAs rápidas).

---

> ### 🔒 Rastro de Segurança & Autoria
>
> Este framework é desenvolvido e mantido por **Wesley Alves**.
>
> 🔗 [Meu Portfólio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> *Qualquer reprodução, distribuição ou uso derivado do framework STARTER deve manter esta atribuição.*  
> **Última atualização:** 2026-06-08
