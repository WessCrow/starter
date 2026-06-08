# RULES.md — Regras Invioláveis (referência humana)

> **Agentes:** hot layer `skills/runtime/rules.yaml` (validado por `schema/rules.schema.json`).  
> **Ordem de carga:** `skills/runtime/index.yaml`.  
> **Este arquivo:** referência humana completa. Sem exceções.

---

## 🚫 Código — O que nunca fazer

- **Zero linhas mortas** — nenhuma variável, import, função ou bloco declarado e não usado
- **Zero `console.log`** em código de produção — usar sistema de logging adequado se necessário
- **Zero `any` explícito** em TypeScript — tipar sempre; se incerto, usar `unknown` com narrowing
- **Zero comentários óbvios** — código deve se auto-explicar; comentar apenas *por quê*, nunca *o quê*
- **Zero `// TODO` sem contexto** — se for deixar, incluir: o quê, por quê, e quando resolver
- **Zero lógica duplicada** — extrair função antes de duplicar
- **Zero `!important` em CSS** — refatorar especificidade em vez de forçar

---

## ✅ Código — O que sempre fazer

- **Funções com responsabilidade única** — se a função faz mais de uma coisa, dividir
- **Nomes descritivos** — `getUserById` não `getU`, `isLoading` não `flag`
- **Constantes nomeadas** para valores mágicos — nunca `if (status === 3)`, sempre `if (status === STATUS.PENDING)`
- **Tratamento de erro explícito** — nunca silenciar um `catch {}` vazio
- **Imports organizados** — externos → internos → relativos, com linha em branco separando grupos

---

## 🌐 HTML / W3C — Semântica obrigatória

### Estrutura
- Usar elementos semânticos: `<header>`, `<main>`, `<nav>`, `<section>`, `<article>`, `<aside>`, `<footer>`
- **Nunca usar `<div>` ou `<span>`** onde existe elemento semântico adequado
- Um único `<h1>` por página — hierarquia de headings nunca quebrada (`h1 → h2 → h3`, nunca pular nível)
- `<title>` descritivo e único por página — nunca genérico como "Home" ou "Page"

### Imagens
- **Alt text obrigatório** em toda `<img>` — nunca vazio (`alt=""`), exceto quando a imagem é puramente decorativa e o elemento pode ser ignorado por leitores de tela
- Alt text descritivo do conteúdo, nunca "imagem de", nunca repetir o texto ao lado
- Imagens decorativas: `alt=""` + `role="presentation"` ou usar CSS background-image

### Links e botões
- Links com texto descritivo — **nunca** "clique aqui", "saiba mais", "leia mais" sem contexto
- `<a>` para navegação, `<button>` para ações — nunca inverter
- Botões com `type="button"` explícito quando não é submit
- Links externos com `rel="noopener noreferrer"` obrigatório

### Formulários
- Cada `<input>` com `<label>` associado via `for`/`id` — nunca usar placeholder como substituto de label
- `<fieldset>` + `<legend>` para grupos de inputs relacionados (radio, checkbox)
- Mensagens de erro associadas ao campo via `aria-describedby`
- Campos obrigatórios marcados com `required` e indicação visual

### Outros
- `lang` obrigatório no `<html>` — `lang="pt-BR"` para projetos em português
- Meta charset e viewport obrigatórios
- Nunca usar `target="_blank"` sem `rel="noopener noreferrer"`

---

## 🎨 CSS / Design — Tokens obrigatórios

- **Zero valores hardcoded** de cor, fonte, espaçamento, border-radius, shadow
- Sempre usar tokens do Design System do projeto (ver `runtime/context.yaml` → `design_system` ou `CONTEXT.md` humano)
- **Zero `px` para font-size** — usar `rem` para respeitar preferências de acessibilidade do usuário
- **Mobile-first obrigatório** — escrever estilos base para mobile, sobrescrever para desktop
- Evitar `position: absolute` e `z-index` sem necessidade — documentar quando inevitável
- **Zero `outline: none`** sem alternativa de foco visível acessível

---

## 🧩 Design System — Regras de uso

- **Antes de criar qualquer componente:** verificar se já existe no Design System do projeto
- Consultar `runtime/context.yaml` → `design_system.components_available` (ou `CONTEXT.md` humano)
- **Nunca improvisar variante** de componente existente — usar as variantes definidas pelo DS
- **Nunca hardcodar** cor, fonte ou espaçamento que existe como token no DS
- Componentes primitivos do DS não devem ser modificados diretamente — criar wrapper se necessário
- Nomear componentes novos respeitando a nomenclatura do DS existente

---

## ♿ Acessibilidade — WCAG AA mínimo obrigatório

### Contraste
- Texto normal: **mínimo 4.5:1** em relação ao fundo
- Texto grande (≥18px regular ou ≥14px bold): **mínimo 3:1**
- Elementos de UI e bordas informativas: **mínimo 3:1**
- Nunca usar cor como único meio de transmitir informação

### Navegação e foco
- **Foco visível em todos os elementos interativos** — nunca remover sem substituto
- Ordem de foco lógica seguindo a ordem visual da página
- Todos os fluxos interativos navegáveis por teclado (Tab, Enter, Esc, setas)
- Skip links para conteúdo principal em páginas com navegação extensa

### ARIA
- **Usar ARIA somente quando HTML semântico não resolve** — ARIA de primeira escolha é anti-padrão
- `aria-label` quando texto visível não descreve suficientemente o elemento
- `aria-describedby` para instruções e erros associados a campos
- `aria-live` para conteúdo que muda dinamicamente sem recarregar página
- `role` somente quando elemento nativo não existe

### Componentes interativos
- Modais: foco aprisionado dentro, fechamento com Esc, foco retorna ao trigger ao fechar
- Dropdowns: navegação por setas, fechamento com Esc
- Toasts/Alertas: `aria-live="polite"` para informações, `aria-live="assertive"` para erros críticos

---

## 📱 Responsividade

- Testar sempre em: 375px (mobile S), 768px (tablet), 1280px (desktop)
- Touch targets mínimo **44×44px** para elementos interativos em mobile
- Nunca usar `vh` em mobile sem fallback — usar `dvh` ou `svh` quando disponível
- Texto nunca menor que **16px** (1rem) em mobile

---

## ⚡ Performance (regras básicas)

- Imagens com `width` e `height` explícitos para evitar layout shift (CLS)
- Imagens abaixo do fold com `loading="lazy"`
- Fontes com `font-display: swap`
- Nunca bloquear o thread principal com loops síncronos pesados

---

## 🔒 Segurança básica & Host Guard (Isolamento)

- **Nunca** expor credenciais, tokens ou chaves em código fonte.
- Sanitizar inputs de usuário antes de renderizar como HTML.
- Nunca usar `dangerouslySetInnerHTML` sem sanitização explícita.
- Variáveis de ambiente: sempre via `.env` e validadas no build.
- **Isolamento de Host:** É terminantemente proibido executar qualquer comando de leitura, escrita ou execução de arquivos fora da árvore de diretórios do workspace do projeto. Comandos como `rm`, `mv` ou `cp` devem ser restritos estritamente ao escopo relativo do repositório.
- Proibido ler chaves SSH (`~/.ssh`), arquivos globais do sistema (`/etc/`) ou diretórios de configurações pessoais do desenvolvedor.

---

## 💻 Pilar Técnico: Front-End (Componentes & Estado)

- **React / Next.js Server Components (RSC) vs Client Components (RCC):**
  * Prefira Server Components por padrão para performance, otimização de bundle e SEO.
  * Use Client Components (`"use client"`) apenas quando houver necessidade de hooks de estado (`useState`, `useEffect`), eventos (`onClick`), ou APIs específicas do browser.
  * Mantenha os Client Components o mais abaixo possível na árvore de componentes (folhas) para evitar hidratações desnecessárias.
- **Prevenção de Re-renders:**
  * Evite declarar funções anonimas inline em propriedades de renderização frequente (ex: `onClick={() => doSomething()}` em loops longos).
  * Use `useMemo` e `useCallback` de forma criteriosa para otimizar componentes filhos caros que dependem de referências de objetos estáveis.
- **Gerenciamento de Estado Previsível:**
  * Para estados locais simples, use hooks nativos do React.
  * Para estado global ou compartilhado complexo, utilize **Zustand** de forma modular, criando seletores específicos (ex: `useUserStore(state => state.profile)`) para evitar renderizações extras.
- **Tokens Semânticos:** Uso estrito de variáveis de CSS semânticas (`--color-bg-primary`, `--color-action-active`) em vez de valores brutos.

---

## ⚙️ Pilar Técnico: Back-End (Segurança & Validação)

- **Validação de Entrada na Borda:**
  * Todo e qualquer dado de entrada em rotas públicas da API (body, query, params) **deve** ser validado imediatamente usando esquemas de validação determinísticos (como **Zod** ou **Joi**). Dados inválidos devem retornar `HTTP 400 Bad Request` instantaneamente, antes de alcançar a lógica de serviço.
- **Sanitização de Erros Públicos (Error Sanitization):**
  * Mensagens de erro de infraestrutura interna ou banco de dados (ex: logs de erro do Prisma, stack traces do Postgres) **nunca** devem ser expostas na resposta HTTP de produção para o cliente. 
  * Retorne mensagens limpas, acionáveis e amigáveis ao usuário, gravando os logs originais detalhados em sistemas internos seguros.
- **Strict Environment Validation:**
  * Valide todas as variáveis de ambiente necessárias no bootstrap da aplicação usando um parser e tipador seguro. O processo deve falhar rápido (`Fail Fast`) no startup caso falte alguma variável obrigatória no `.env`.

---

## 📐 Pilar Técnico: Arquitetura & SOLID

- **SOLID (Responsabilidade Única e Inversão de Dependência):**
  * Cada módulo, classe ou arquivo deve ter apenas **um único motivo para mudar** (Single Responsibility).
  * Lógica de negócios de alto nível nunca deve depender diretamente de módulos de infraestrutura de baixo nível (ex: banco de dados, provedor de e-mail). Ambos devem depender de abstrações (interfaces/ports).
- **Acoplamento Cíclico Zero:**
  * É proibido criar dependências circulares entre módulos ou camadas (ex: Módulo A importa Módulo B, que por sua vez importa o Módulo A). Use injeção de dependência ou interfaces para quebrar ciclos.
- **Domínio Puro (Pure Domain):**
  * A camada de lógica de negócios (entidades e regras de domínio) deve ser puramente agnóstica de frameworks e tecnologias de entrega (Express, Nest.js, Fastify). Ela deve persistir pura e testável isoladamente.

---

> **Lembrete:** estas regras não são sugestões. São critérios de aceite.
> Código que viola qualquer regra acima não está pronto para entrega.

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-08
