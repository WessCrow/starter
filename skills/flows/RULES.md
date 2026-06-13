# RULES.md — Regras Invioláveis

> **Agentes:** hot layer `runtime/rules.yaml` · Ordem: `runtime/index.yaml` · Este arquivo: referência humana. Sem exceções.

---

## Código — Proibido

| Regra | Detalhe |
|-------|---------|
| Zero linhas mortas | Nenhuma variável/import/função declarada e não usada |
| Zero `console.log` em produção | Usar sistema de logging adequado |
| Zero `any` em TypeScript | Usar `unknown` com narrowing |
| Zero comentários óbvios | Comentar apenas *por quê*, nunca *o quê* |
| Zero `// TODO` sem contexto | Incluir: o quê, por quê, quando |
| Zero lógica duplicada | Extrair função antes de duplicar |
| Zero `!important` em CSS | Refatorar especificidade |

## Código — Obrigatório

| Regra | Detalhe |
|-------|---------|
| Responsabilidade única | Se a função faz mais de uma coisa, dividir |
| Nomes descritivos | `getUserById` não `getU`; `isLoading` não `flag` |
| Constantes nomeadas | `STATUS.PENDING`, nunca `3` |
| Tratamento de erro explícito | Nunca `catch {}` vazio |
| Imports organizados | externos → internos → relativos, separados por linha em branco |

---

## HTML / Semântica

| Regra | Detalhe |
|-------|---------|
| Elementos semânticos | `<header>`, `<main>`, `<nav>`, `<section>`, `<article>`, `<aside>`, `<footer>` |
| Um `<h1>` por página | Hierarquia nunca quebrada (h1→h2→h3) |
| Alt text obrigatório | Descritivo; decorativa: `alt=""` + `role="presentation"` |
| Links descritivos | Nunca "clique aqui" sem contexto |
| `<a>` para nav / `<button>` para ação | Nunca inverter |
| Links externos | `rel="noopener noreferrer"` obrigatório |
| Formulários | `<label>` via `for`/`id`; erros via `aria-describedby`; `required` marcado |
| `lang` no `<html>` | `lang="pt-BR"` para projetos PT |
| `target="_blank"` | Sempre com `rel="noopener noreferrer"` |

---

## CSS / Design Tokens

| Regra | Detalhe |
|-------|---------|
| Zero valores hardcoded | Cor, fonte, espaçamento, radius, shadow → tokens do DS |
| Zero `px` em font-size | Usar `rem` |
| Mobile-first obrigatório | Base mobile, sobrescrever para desktop |
| Zero `outline: none` | Sem alternativa de foco visível acessível |

---

## Design System

- Verificar componente existente antes de criar novo (`context.yaml → design_system.components_available`)
- Nunca improvisar variante de componente — usar variantes definidas
- Nunca modificar primitivos do DS diretamente — criar wrapper
- Nomear novos componentes respeitando nomenclatura do DS

---

## Acessibilidade — WCAG AA mínimo

| Critério | Regra |
|----------|-------|
| Contraste texto normal | mínimo 4.5:1 |
| Contraste texto grande (≥18px / ≥14px bold) | mínimo 3:1 |
| Elementos de UI / bordas | mínimo 3:1 |
| Cor como informação | Nunca única forma de transmitir |
| Foco visível | Todos os elementos interativos — nunca remover sem substituto |
| Ordem de foco | Lógica, seguindo ordem visual |
| Navegação por teclado | Tab, Enter, Esc, setas em todos os fluxos |
| ARIA | Somente quando HTML semântico não resolve |
| Modais | Foco aprisionado; Esc fecha; foco retorna ao trigger |
| `aria-live` | "polite" para info; "assertive" para erros críticos |

---

## Responsividade

- Testar: 375px · 768px · 1280px
- Touch targets: mínimo 44×44px em mobile
- `vh` em mobile: usar `dvh` ou `svh` como fallback
- Texto: nunca < 16px (1rem) em mobile

---

## Performance

- Imagens: `width` + `height` explícitos (evita CLS); `loading="lazy"` abaixo do fold
- Fontes: `font-display: swap`
- Nunca bloquear thread principal com loops síncronos pesados

---

## Segurança & Host Guard

| Proibido |
|----------|
| Expor credenciais/tokens em código fonte |
| `dangerouslySetInnerHTML` sem sanitização |
| Inputs renderizados como HTML sem sanitização |
| Variáveis de ambiente fora de `.env` validado |
| Comandos `rm`/`mv`/`cp` fora do escopo relativo do repositório |
| Ler `~/.ssh`, `/etc/` ou configs pessoais do SO |

---

## React / Next.js

| Regra | Detalhe |
|-------|---------|
| Server Components por padrão | `"use client"` só com hooks de estado/eventos/browser API |
| Client Components nas folhas | Evitar hidratações desnecessárias |
| `useMemo`/`useCallback` criterioso | Só para componentes filhos caros com referências estáveis |
| Estado global | Zustand modular com seletores específicos |
| Tokens semânticos | `--color-bg-primary`, nunca valores brutos |

---

## Back-End

| Regra | Detalhe |
|-------|---------|
| Validação na borda | Zod/Joi em toda rota pública; dados inválidos → HTTP 400 antes da lógica |
| Sanitização de erros | Stack traces/DB errors nunca expostos ao cliente |
| Env vars validadas no startup | Fail Fast se variável obrigatória ausente |

---

## Arquitetura & SOLID

| Princípio | Regra |
|-----------|-------|
| Responsabilidade única | Um módulo = um motivo para mudar |
| Inversão de dependência | Lógica de negócio não depende de infra — abstrações/interfaces |
| Acoplamento cíclico zero | A importa B importa A = proibido |
| Domínio puro | Entidades e regras agnósticas de framework |

---

> **Lembrete:** estas regras são critérios de aceite. Código que viola qualquer regra não está pronto para entrega.

---

> **Autoria:** Wesley Alves · [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · Última atualização: 2026-06-11
