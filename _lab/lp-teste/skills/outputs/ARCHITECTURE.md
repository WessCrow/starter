# ARCHITECTURE — NutriLeve

## Decisão: Stack React + Vite
**Data:** 2026-06-09
**Stack:** React 18 + Vite 5 + TypeScript + Tailwind 3 + pnpm
**Estrutura:** react-vite-structure.skill aplicada
**Alias:** @/ → src/
**Convenções:** PascalCase componentes, use* hooks, kebab-case pastas

## Decisão: CTA via wa.me sem backend
**Data:** 2026-06-09
**Contexto:** usuária pediu contato direto no WhatsApp; v1 sem servidor.
**Decisão:** link `wa.me` com mensagem pré-preenchida; número via `VITE_WHATSAPP_NUMBER`.
**Consequências:** zero custo de infra; troca de número é alteração de env, não de código.

## Decisão: Tailwind puro (sem shadcn) na v1
**Data:** 2026-06-09
**Contexto:** landing estática, sem formulários ou componentes complexos.
**Decisão:** tokens de cor próprios (`leaf`) no tailwind.config.
**Consequências:** menos dependências; shadcn pode entrar se v2 tiver UI interativa.
