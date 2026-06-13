# prompt-engineering.md — Regras de Prompt para Designers

> **Papel:** Define como estruturar prompts para IA em contextos de design  
> **Fonte:** Princípios práticos condensados de uso real como Head of Product Design  
> **Aplicação:** Toda vez que a tarefa é gerar um prompt, revisar um prompt, ou usar a `prompt-library`  
> **Versão:** 1.0 — incorporado em 2026-05-15

---

## 🔒 Regra fundamental — leia antes de qualquer prompt

> **Prompt bom acelera designer que pensa. Não substitui o pensamento.**

IA amplifica quem você é. Se usa pra pular raciocínio, atrofia. Se usa pra acelerar o raciocínio que já faz, cresce.

---

## 🚫 Zero persona triggers

**Nunca começar prompt com:**
```
"Você é um especialista sênior em X com 10 anos de experiência em Y"
"Assuma o papel de..."
"Aja como se você fosse..."
```

**Por quê:** Cada palavra é token pago. E não muda o resultado.  
Modelos atuais (Claude, GPT-4) já operam em nível de especialista por padrão.  
**O que muda o output é contexto específico e formato de entrega — não persona assumida.**

**Correto:**
```
## Contexto
Produto: [descrever brevemente]
Público: [descrever]
Momento do fluxo: [onde isso aparece]
```

---

## 🧱 A estrutura que funciona — 4 blocos obrigatórios

Todo prompt deve seguir exatamente esta ordem:

```markdown
## Contexto
[Curto, factual, sem adjetivos. O que a IA precisa saber pra não errar o alvo.]

## Ações
[Lista direta e numerada do que a IA deve fazer. Verbos no imperativo.]

## Expectativa
[Por que você precisa disso. Como vai usar o output. O que NÃO quer receber.]

## Formato de entrega
[Estrutura exata da resposta — blocos markdown prontos pra copiar e usar.]
```

**Regra crítica:** Formato de entrega é a parte que mais economiza tempo depois.  
Se você diz como quer receber, recebe pronto pra usar.  
Se não diz, perde tempo reformatando.

---

## 📐 Princípios de qualidade

### Contexto
- Factual, não descritivo. "produto de controle financeiro para freelancers" — não "um produto moderno e inovador"
- Incluir exemplos e links — dão mais contexto que adjetivos
- Máximo necessário — não mínimo possível, não máximo possível

### Ações
- Uma ação por linha
- Verbo no imperativo: "Extrair", "Gerar", "Avaliar", "Reformular"
- Se houver quantidade, especificar: "Gerar 5 hipóteses", "Listar 3 variações"

### Expectativa
- Explica o uso real do output: "Vou apresentar pro time de produto"
- Pode incluir restrições: "Não quero respostas. Só as perguntas."
- Pode incluir contexto emocional: "Vou ter reunião amanhã. Preciso decidir antes."

### Formato de entrega
- Usar blocos de código markdown com a estrutura esperada
- Incluir placeholders `[entre colchetes]` onde a IA deve preencher
- Especificar nível: "máximo 150 palavras por versão", "3 variações"

---

## 🎨 Regra extra para prompts visuais

Se a tarefa envolve interface, landing page, hero, dashboard ou direção estética, o prompt inicial deve incluir:

- referências visuais ou estilo nomeado
- contraste / densidade esperados
- tipografia ou tom visual
- comportamento de cor
- o que deve ser evitado
- nível de fidelidade esperado

Se essa direção ainda não estiver clara, usar `visual-direction-brief` antes de escrever o prompt principal.

Exemplo ruim:

```text
faz uma landing premium
```

Exemplo melhor:

```text
crie uma landing com alto contraste, composição editorial, tipografia dominante, poucas cores, sensação sofisticada e zero aparência de template SaaS genérico
```

---

## 🔁 Refinamento seguro

Ao iterar, prefira preservar o que já funcionou:

- "mantenha a estrutura e ajuste só a hierarquia visual"
- "preserve a paleta e refine apenas a tipografia"
- "não refaça a página; melhore só o hero"

Evite prompts meta vagos como:

- "reconsidera"
- "repensa tudo"
- "faz melhor"

Esses prompts tendem a quebrar o contexto visual já construído.

---

## 🔁 Como usar a prompt-library

A skill `catalog/prompt-library.skill` contém 20 prompts prontos em 5 categorias:

| Categoria | Quando usar |
|---|---|
| **Pesquisa e insights** | Entrevistas, síntese, hipóteses, guia de pesquisa |
| **Escrita e microcopy** | Simplificação, CTAs, erros, voz e tom |
| **Crítica e revisão** | Fluxo, decisão, vieses, portfolio |
| **Ideação e exploração** | Brainstorm, desbloqueio, referências, briefing |
| **Carreira e comunicação** | Entrevista, emails difíceis, feedback, reflexão |

**Uso correto:**
1. Abrir a categoria correspondente
2. Copiar o prompt completo
3. Substituir os `[placeholders]` com contexto real
4. Ajustar se o output não sair bom — refinar a estrutura, não adicionar persona

---

## ✅ Checklist antes de enviar qualquer prompt

```
[ ] Zero persona trigger na abertura
[ ] Contexto factual e específico (sem adjetivos vagos)
[ ] Ações em lista com verbo imperativo
[ ] Expectativa inclui como o output será usado
[ ] Formato de entrega especificado em markdown
[ ] Sem adjetivos que a IA vai ignorar de qualquer forma
```

---

## 🧪 Como saber se o prompt funcionou

Output bom:
- Estruturado exatamente como pedido
- Acionável — não precisa reformatar para usar
- Você gasta pouco tempo editando

Output ruim:
- Genérico, vago, "parece uma IA"
- Precisa de muito trabalho para ficar utilizável
- **Solução:** voltar ao prompt e refinar a estrutura — não adicionar mais contexto aleatório

---

> **Nota:** Markdown é melhor formato que docx ou pdf para trabalhar com IA.  
> Mais leve, estruturado, sem formatação escondida, reutilizável como rotina.

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07
