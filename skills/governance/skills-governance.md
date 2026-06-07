# skills-governance.md — Decisão Operacional de Skills (Sprint 1)

> **Papel:** definir o que é capacidade real, capacidade adiada e capacidade futura no STARTER  
> **Status:** decisão ativa a partir de 2026-05-26  
> **Escopo:** catálogo, roteamento, fallback remoto e prioridade de fonte da verdade

---

## Objetivo desta sprint

Fechar a ambiguidade sobre o sistema de skills **antes** de sanear documentação e **antes** de criar skill nova.

Esta decisão existe para responder, sem interpretação:

- o que o STARTER suporta hoje de verdade
- o que está adiado
- o que é apenas intenção futura
- qual arquivo manda em cada tipo de decisão

Enquanto a Sprint 2 não terminar, este documento **prevalece** sobre descrições ambíguas em outros arquivos.

---

## Decisão principal

O STARTER passa a operar com **3 classes de capacidade**:

### 1. Capacidade ativa

É tudo que pode entrar no fluxo normal hoje.

Inclui:

- `skills/local-skills/*.skill`
- `skills/structure/*.skill`
- docs operacionais locais já existentes em `skills/governance/`

### 2. Capacidade adiada

Existe no repositório, mas **não** entra no fluxo padrão.

Inclui:

- `skills/_deferred/**`

Regra:

- itens em `_deferred` não podem aparecer como opção prioritária no roteamento ativo

### 3. Capacidade futura

É intenção arquitetural, mas **não** pode ser tratada como suporte operacional atual.

Inclui:

- `skills/linked-skills/`
- `skills/cache/`
- fallback por `skills.sh`

Regra:

- enquanto não houver implementação real e política explícita de uso, esses itens são **futuros**, não ativos

---

## Decisões específicas

### `linked-skills/`

**Decisão:** permanece como diretório reservado para integrações futuras por symlink, mas não faz parte da capacidade ativa do STARTER nesta fase.

Implicações:

- diretório vazio não conta como suporte existente
- skill remota só existe quando houver arquivo real apontando para destino válido
- o roteamento não deve depender de `linked-skills/` até a Sprint 2 saneá-lo

### `skills.sh`

**Decisão:** fallback remoto por `skills.sh` está **desligado como capacidade operacional**.

Implicações:

- pode continuar citado como direção futura, mas não como fluxo confiável do sistema
- nenhuma execução crítica deve depender dele
- a reativação só pode acontecer com documentação, política de cache e validação

### `cache/`

**Decisão:** `skills/cache/` não é fonte operacional de skills neste momento.

Implicações:

- cache vazio não é erro estrutural
- o sistema não pode anunciar cache remoto funcional sem implementação real
- uso de cache remoto depende de política formal posterior

### `_deferred/`

**Decisão:** `_deferred` é área de incubação, não de roteamento.

Implicações:

- conteúdo em `_deferred` pode ser mantido no repo
- conteúdo em `_deferred` não deve ser promovido implicitamente a capability ativa

---

## Fonte da verdade por camada

Para reduzir conflito entre arquivos, a hierarquia operacional fica assim:

### Execução em runtime

**Arquivo principal:** `skills/governance/Start-ops.md`

Função:

- orchestrator compacto da sessão
- define o fluxo operacional real durante uso normal

### Roteamento de skills

**Arquivo principal:** `skills/governance/Start.md`

Função:

- matriz de resolução e roteamento
- referência de escolha entre skills

Regra:

- após a Sprint 2, `Start.md` deve listar apenas capability ativa ou capability explicitamente marcada como futura/adiada

### Catálogo humano

**Arquivo principal:** `skills/README.md`

Função:

- visão humana do sistema
- descrição resumida das skills disponíveis

Regra:

- `README.md` não define verdade operacional sozinho
- se houver conflito, prevalecem filesystem + esta decisão + `Start.md`

### Navegação rápida

**Arquivo principal:** `skills/INDEX.md`

Função:

- entrypoint curto para localizar docs centrais

### Estrutura física

**Arquivo principal:** `skills/STRUCTURE.md`

Função:

- mapa de diretórios e convenções de organização

Regra:

- `STRUCTURE.md` descreve a arquitetura esperada, mas não prova que uma capability está ativa

---

## Regra de precedência até a Sprint 2

Se houver conflito entre documentação e diretório real:

1. filesystem real
2. este arquivo
3. `Start-ops.md`
4. `Start.md`
5. `README.md`
6. `INDEX.md`
7. `STRUCTURE.md`

Objetivo:

- impedir que capacidade aspiracional seja tratada como capacidade pronta

---

## Critério para ativar capability futura

Uma capability hoje marcada como futura só pode virar ativa quando cumprir **todos** os itens abaixo:

- existir fisicamente no repositório
- ter propósito documentado
- ter política de uso clara
- aparecer de forma consistente no roteamento
- passar por validação automática na Sprint 3

Sem isso, continua futura.

---

## Decisão sobre expansão nesta fase

Nenhuma nova skill funcional deve ser criada antes de:

1. sanear o roteamento
2. sanear a documentação central
3. criar mecanismo de antidrift

Consequência:

- a `visual-direction-brief.skill` continua válida como lacuna funcional
- mas fica explicitamente **fora da Sprint 1**

---

## Resultado esperado desta sprint

Ao final da Sprint 1, o projeto passa a ter uma resposta objetiva para:

- o que está ativo
- o que está adiado
- o que é futuro
- qual arquivo manda em cada camada

As próximas sprints agora podem atacar saneamento e validação sem discutir premissas de novo.

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07
