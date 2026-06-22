# spec.md — Aprendizado Contínuo (Double-Loop Learning)

> **Feature:** 012-continuous-learning
> **Projeto:** STARTER
> **Criado em:** 2026-06-19
> **Status:** aprovado
> **Protocolo:** `skills/flows/feature-flow.md`

---

## Por quê

Evitar a regressão e o retrabalho em sessões recorrentes do agente, capturando correções humanas feitas nos arquivos e transformando-as em melhorias permanentes nas diretivas do sistema (skills). Sem registros, não há aprendizado operacional; sem um avaliador, não há confiança nos patches autônomos.

---

## Histórias de usuário

| # | Como… | Quero… | Para… | Prioridade |
|---|-------|--------|-------|------------|
| H1 | Agente de IA (Loop 1) | Registrar automaticamente os inputs, decisões e diffs gerados após cada execução | Rastrear o comportamento inicial e permitir auditoria | alta |
| H2 | Mantenedor do projeto | Executar um agente analítico (Loop 2) que compare logs contra correções de humanos | Identificar desalinhamentos operacionais e sugerir correções de skills | alta |
| H3 | Engenheiro de Design | Garantir que as propostas do Loop 2 passem por validações rigorosas antes do merge | Evitar regressões silenciosas nas regras da equipe | alta |

---

## Critérios de aceite (testáveis)

1. Ao encerrar a sessão (ou rodar QA Gate), o sistema grava em um arquivo JSONL ou YAML o trace da execução sob `qa/runs/`.
2. O agente do Loop 2 compara o trace com as modificações finais encontradas no repositório (via git log/status) e identifica quais arquivos foram alterados por humanos após a atuação do agente.
3. Se houver desvio, o Loop 2 propõe uma modificação focada no arquivo `.skill` relevante, escrevendo uma justificativa explicável.
4. Qualquer alteração gerada passa obrigatoriamente pela validação estrutural (`validate-skills.py`).
5. A aplicação do patch respeita o nível configurado no seletor de autonomia (Autonomy Dial).

---

## Fora do escopo

- Integração externa com APIs de Slack ou GitHub nesta sprint (logs locais apenas).
- Execuções paralelas distribuídas fora do ambiente local do workspace.

---

## Clarificações

| Data | Pergunta | Resposta |
|------|----------|----------|
| 2026-06-19 | Onde serão salvos os traces? | Localmente na pasta `qa/runs/`, ignorados no Git. |
| 2026-06-19 | Como o patch será validado? | Através do script `validate-skills.py` + aprovação opcional via CLI do usuário. |

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: 2026-06-19

## Análise de Riscos

- **Risco:** Geração de patches infinitos ou loop de correções de skills contraditórias entre execuções diferentes.
  - **Mitigação:** Registro histórico de decisões de aprendizado em decisions.yaml e regras estritas de não-sobrescrita em skills consolidadas.
