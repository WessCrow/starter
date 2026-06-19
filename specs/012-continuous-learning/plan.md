# plan.md — Aprendizado Contínuo (Double-Loop Learning)

> **Feature:** 012-continuous-learning
> **Baseado em:** `spec.md` (status: aprovado)
> **Criado em:** 2026-06-19
> **Protocolo:** `skills/flows/feature-flow.md`

---

## Stack e dependências

- Stack do projeto: Python 3 para scripts de infraestrutura (`validate-skills.py`, etc.).
- Novas dependências: Nenhuma dependência externa. Usaremos a biblioteca padrão do Python (`json`, `subprocess`, `pathlib`, `datetime`).

---

## Modelo de dados

Os logs de execução (traces) do Loop 1 serão salvos em `qa/runs/session-[timestamp].jsonl`. A estrutura conceitual do log será:

```json
{
  "timestamp": "ISO-8601",
  "session_id": "string",
  "feature_id": "string",
  "commands_run": [
    {
      "command": "string",
      "exit_code": 0,
      "output_snippet": "string"
    }
  ],
  "agent_diff": "string",
  "files_touched": ["string"]
}
```

---

## Arquitetura da feature

Arquivos novos:
- `skills/flows/continuous-learning.md` (Diretrizes de processo)
- `skills/catalog/learn.skill` (Instruções conceituais de aprendizado)
- `skills/infra/scripts/record_session.py` (Script de gravação de sessões)
- `skills/infra/scripts/continuous_learner.py` (Script consolidador/analítico)

Modificados:
- `skills/infra/scripts/validate-skills.py` (Regras adicionais de validação)

---

## Nível arquitetural

- **Nível:** [ ] S  [x] M  [ ] L  [ ] XL
- **Justificativa:** Trata-se de uma funcionalidade autocontida baseada em scripts utilitários em Python instalados na pasta de infraestrutura (`skills/infra/scripts/`) sem a criação de novos frameworks ou serviços de banco de dados pesados.
- **Descartado:** Banco de dados SQLite descartado: a persistência via arquivos estruturados `.jsonl` em `qa/runs/` é suficiente para análise local sem adicionar overhead ou dependências extras de conexão/schema.

---

## Riscos e decisões

| Decisão | Rastreia para (critério do spec.md) | Alternativa descartada | Motivo |
|---------|--------------------------------------|------------------------|--------|
| Armazenar diffs e traces em arquivos JSONL locais | Critério 1 (gravar trace) | Armazenar em DB relacional ou log centralizado | Complexidade de dependências e perda de simplicidade local |
| Executar `validate-skills.py` de forma obrigatória antes de sugerir patch | Critério 4 (validação de regressão) | Validar manualmente no chat | Facilidade de introdução de erros de formatação ou estouro de tokens sem verificação local determinística |

---

## Constitution check

- [x] Nenhuma regra de segurança violada (Host Guard: todas as escritas e leituras limitadas à árvore do workspace).
- [x] Padrões de código e acessibilidade respeitados.
- [x] Sem dependência ou complexidade não justificada pelo spec.

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
> Última atualização: 2026-06-19
