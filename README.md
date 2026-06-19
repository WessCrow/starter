# STARTER

> **Um framework de governança e regras para agentes de IA (como Claude, Cursor, Gemini, Antigravity) construírem projetos de software estruturados, seguros e consistentes.**

[![Runtime](https://img.shields.io/badge/Runtime-v5.5-8B5CF6?style=flat-square&logo=yaml&logoColor=white)](skills/core/runtime/index.yaml)
[![QA Gate](https://img.shields.io/badge/QA_Gate-Ativo-10B981?style=flat-square&logo=github-actions&logoColor=white)](skills/catalog/qa-smoke.skill)
[![Host Guard](https://img.shields.io/badge/Host_Guard-Protegido-EF4444?style=flat-square&logo=shield&logoColor=white)](skills/flows/host-guard.md)

---

## 🎯 O que é o STARTER?

O STARTER é a **camada de governança e inteligência local** que dita as regras de como o agente de IA interage com o seu código. Ele impede que a IA pule etapas, apague arquivos acidentalmente, cometa códigos sem testar ou tome decisões técnicas sem o seu consentimento.

---

## ⚡ Como Usar em 3 Passos

1. Copie a pasta [skills/](skills) e o arquivo [AGENTS.md](AGENTS.md) para a raiz do seu novo projeto.
2. No chat do editor (Cursor, Antigravity, Claude Code, etc.), digite: **`Começar projeto`**.
3. Responda às breves perguntas de direcionamento do agente, aprove o resumo da arquitetura e pronto!

---

## 🏛️ Estrutura Mínima

```text
seu-projeto/
├── AGENTS.md             ← Regras de comportamento e orquestração do agente
├── COMECAR-PROJETO.md    ← Instruções rápidas de uso
├── README.md             ← Documentação essencial do repositório
└── skills/
    ├── core/runtime/     ← Arquivos YAML de estado (hot/warm/cold) e Schemas
    ├── catalog/          ← Skills funcionais nativas (QA, TDD, Design)
    ├── flows/            ← Protocolos e guias de fluxo obrigatórios
    ├── structure/        ← Arquitetura de diretórios recomendada por stack
    ├── templates/        ← Modelos de especificação, contratos e scripts
    └── infra/            ← Validadores internos e scripts de proteção
```

---

## 🛠️ Recursos de Destaque

*   **Host Guard & Pre-commit Hooks:** Proteção ativa contra comandos destrutivos (`rm -rf`) ou vazamento de chaves secretas.
*   **Protocolo Spec-driven:** Fluxo de desenvolvimento baseado em especificações estruturadas antes da escrita de qualquer linha de código.
*   **QA Gate & Verificação Contínua:** Verificações automáticas de sanidade e integração E2E via Playwright (**Fase 4**).
*   **Orquestração & Autonomia Inteligente:** Daemon local nativo para execução assíncrona controlada e otimização inteligente de tokens.

---

> Mantido por **Wesley Alves**.
> 🔗 [Portfólio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
