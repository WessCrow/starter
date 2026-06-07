## Contexto

Marca: [NOME DA MARCA]
File Key Figma: [FILE_KEY]

Cores da marca:
- Primária: [HEX]
- Secundária: [HEX ou null]
- Neutro base: [HEX]

Tipografia:
- Font Display: [fonte]
- Font Body: [fonte]

Pré-condições de execução:
- usar `use_figma` para writes no Figma
- verificar disponibilidade das fontes antes de criar text styles
- se uma fonte não existir, usar `Inter` como fallback e registrar no output
- se `use_figma` não estiver disponível, parar e retornar bloqueio

## Ações

1. Validar os inputs obrigatórios e interromper se faltar `fileKey` ou qualquer dado crítico da marca.
2. Executar em blocos sequenciais para evitar timeout:
   - bloco A: fontes, collections e preparação
   - bloco B: variáveis de cor
   - bloco C: text styles e spacing
   - bloco D: página Foundation e resumo final
3. Criar ou reutilizar uma variable collection chamada `Colors`.
4. Na collection `Colors`, criar os grupos:
   - `Primary`: `primary-50`, `primary-100`, `primary-200`, `primary-300`, `primary-400`, `primary-500`, `primary-600`, `primary-700`, `primary-800`, `primary-900`, `primary-950`
   - `Secondary`: só criar se a cor secundária existir, com a mesma estrutura `50` até `950`
   - `Gray`: `gray-50`, `gray-100`, `gray-200`, `gray-300`, `gray-400`, `gray-500`, `gray-600`, `gray-700`, `gray-800`, `gray-900`, `gray-950`
   - auxiliares fixas:
     - success-50 `#f0fdf4`
     - success-100 `#dcfce7`
     - success-500 `#22c55e`
     - success-600 `#16a34a`
     - success-700 `#15803d`
     - warning-50 `#fffbeb`
     - warning-100 `#fef3c7`
     - warning-500 `#f59e0b`
     - warning-600 `#d97706`
     - warning-700 `#b45309`
     - error-50 `#fef2f2`
     - error-100 `#fee2e2`
     - error-500 `#ef4444`
     - error-600 `#dc2626`
     - error-700 `#b91c1c`
     - info-50 `#eff6ff`
     - info-100 `#dbeafe`
     - info-500 `#3b82f6`
     - info-600 `#2563eb`
     - info-700 `#1d4ed8`
5. Criar todas as variáveis de cor com type `"COLOR"`.
6. Gerar as escalas `Primary`, `Secondary` e `Gray` usando HSL com esta regra:
   - `500` = cor base exata informada
   - `50` a `400`: aumentar lightness progressivamente e reduzir saturação entre `10%` e `30%` nos tons mais claros para evitar neon
   - `600` a `950`: diminuir lightness progressivamente e manter saturação estável ou com leve queda
   - clamp de lightness entre `4` e `98`
   - clamp de saturação entre `2` e `100`
7. Criar ou reutilizar uma variable collection chamada `Spacing`.
8. Criar as variáveis float:
   - `spacing-0 = 0`
   - `spacing-1 = 4`
   - `spacing-2 = 8`
   - `spacing-3 = 12`
   - `spacing-4 = 16`
   - `spacing-5 = 20`
   - `spacing-6 = 24`
   - `spacing-7 = 28`
   - `spacing-8 = 32`
   - `spacing-10 = 40`
   - `spacing-12 = 48`
   - `spacing-14 = 56`
   - `spacing-16 = 64`
   - `spacing-20 = 80`
   - `spacing-24 = 96`
   - `spacing-32 = 128`
9. Criar todos os text styles com `figma.createTextStyle()`.
10. Para `Display/`, usar a fonte display com fallback para `Inter` se necessário:
   - `Display/2xl`: 72px, line-height 1.1, weight 700
   - `Display/xl`: 60px, line-height 1.1, weight 700
   - `Display/lg`: 48px, line-height 1.15, weight 700
   - `Display/md`: 36px, line-height 1.2, weight 600
   - `Display/sm`: 30px, line-height 1.25, weight 600
   - `Display/xs`: 24px, line-height 1.3, weight 600
11. Para `Text/`, usar a fonte body com fallback para `Inter` se necessário:
   - `Text/xl`: 20px, line-height 1.5
   - `Text/lg`: 18px, line-height 1.5
   - `Text/md`: 16px, line-height 1.5
   - `Text/sm`: 14px, line-height 1.4
   - `Text/xs`: 12px, line-height 1.4
12. Para cada tamanho `Text/`, criar:
   - regular `400` com nome base, por exemplo `Text/md`
   - medium `500` com nome `Text/md Medium`
   - semibold `600` com nome `Text/md Semibold`
13. Criar uma nova página chamada `🎨 Foundation`.
14. Executar `await figma.setCurrentPageAsync(novaPage)` antes de criar qualquer frame nela.
15. Criar os frames `Colors`, `Typography` e `Spacing` com:
   - largura `1200`
   - altura hug
   - fundo `#F8F9FA`
   - padding interno `48`
   - gap entre seções `32`
16. No frame `Colors`, exibir todos os grupos com swatches:
   - cada swatch deve ter retângulo `80x80`
   - nome do token abaixo em `Text/sm`
   - valor abaixo em `Text/xs` com `gray-400`
   - labels de grupo em `Display/xs`
17. Ao criar os swatches, não usar fill hardcoded. Buscar a variável pelo id e aplicar alias no fill:

```ts
node.fills = [
  {
    type: 'SOLID',
    color: { r: 0, g: 0, b: 0 },
    boundVariables: {
      color: { type: 'VARIABLE_ALIAS', id: variable.id },
    },
  },
]
```

18. Se o valor resolvido da variável não estiver acessível facilmente para o label inferior, exibir o nome do token no lugar do hex.
19. No frame `Typography`, criar duas seções:
   - `Display`
   - `Text`
20. Para cada text style no frame `Typography`, mostrar:
   - nome do estilo em `Text/sm` com `gray-400`
   - exemplo `The quick brown fox` com o próprio estilo aplicado
21. No frame `Spacing`, para cada token:
   - label à esquerda em `Text/sm`
   - barra horizontal com largura igual ao valor do token
   - valor à direita em `Text/xs` com `gray-400`
   - usar `primary-200` na barra
22. Preferir reutilizar ou atualizar itens existentes quando o nome coincidir, em vez de duplicar collections, variables, styles ou página.

## Expectativa

Vou usar isso como base oficial de foundation no arquivo Figma da marca.

Quero:
- collections limpas e nomeadas de forma consistente
- text styles prontos para uso
- página de documentação navegável
- zero camelCase
- zero fills hardcoded nos swatches
- resumo final com contagem objetiva do que foi criado

Se houver bloqueio de tool, fonte ou permissão, parar e reportar isso claramente em vez de inventar execução parcial silenciosa.

## Formato de entrega

```markdown
✅ [X] variáveis de cor criadas
✅ [X] variáveis de spacing criadas
✅ [X] text styles criados
✅ Página Foundation criada com [X] frames
⚠️ Fontes substituídas por fallback: [lista ou "nenhuma"]
```

Se não der para executar:

```markdown
⚠️ Bloqueio
- Motivo: [motivo objetivo]
- Falta: [tool, permissão, fonte ou dado]
- Próximo passo: [ação clara para destravar]
```

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07
