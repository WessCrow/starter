#!/usr/bin/env bash
# session-start-hook.sh — Hook de início de sessão do STARTER (opt-in)
#
# Transforma o bootstrap do AGENTS.md de convenção em garantia: injeta o
# protocolo de carga no contexto do agente em TODA sessão, automaticamente.
# Inspirado no hook session-start do obra/superpowers.
#
# Suporte: Claude Code (hooks SessionStart). Outros editores (Cursor, Windsurf,
# Cline) seguem lendo AGENTS.md normalmente — este hook é um reforço, não um
# requisito.
#
# Como ativar no Claude Code — adicionar ao .claude/settings.json do projeto:
# {
#   "hooks": {
#     "SessionStart": [
#       { "hooks": [ { "type": "command",
#         "command": "bash skills/scripts/session-start-hook.sh" } ] }
#     ]
#   }
# }

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

CONTEXT="STARTER Runtime OS ativo. Antes de responder qualquer pedido:
1. Carregar skills/runtime/index.yaml (hot: rules.yaml, context.yaml, state.yaml).
2. Seguir skills/governance/Start-ops.md como orchestrator da sessao.
3. 'Comecar projeto' -> skills/governance/kickoff.md. Nova feature -> skills/governance/feature-flow.md (HARD-GATE: sem codigo antes de contrato aprovado).
4. Bug/erro -> skills/governance/debugging-protocol.md. Feedback/critica -> skills/governance/review-reception.md.
5. Nunca afirmar 'pronto/corrigido' sem evidencia: skills/local-skills/verify-before-done.skill.
6. Pos-implementacao: qa-gate.skill + qa-smoke.skill obrigatorios.
7. Fim de atividade pesada (feature/kickoff/sprint): session-review.skill (4 blocos, relatorio em docs/private/reviews/).
8. Idioma do projeto: respeitar runtime/context.yaml -> language (docs/product).
9. Pos-sessao: atualizar handoff.yaml + state.yaml, validate.py com 0 failed."

# Sanidade: avisar se a estrutura não existe (hook copiado para projeto sem skills/)
if [ ! -f "${REPO_ROOT}/skills/runtime/index.yaml" ]; then
  CONTEXT="AVISO: skills/runtime/index.yaml nao encontrado. Estrutura STARTER incompleta — verificar se a pasta skills/ foi copiada."
fi

# Pipeline de incubação: lembrar se há candidatas TESTAR_ aguardando (skill-intake.md)
INTAKE_DIR="${REPO_ROOT}/docs/private/_novas skills"
if [ -d "$INTAKE_DIR" ]; then
  pending_count=$(find "$INTAKE_DIR" -maxdepth 1 -name 'TESTAR_*' -type f 2>/dev/null | wc -l | tr -d ' ')
  if [ "$pending_count" -gt 0 ]; then
    CONTEXT="${CONTEXT}
LEMBRETE: ${pending_count} skill(s) candidata(s) TESTAR_ aguardando avaliacao em docs/private/_novas skills/ — protocolo: skills/governance/skill-intake.md."
  fi
fi

# Escapar para JSON
escape_for_json() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\n'/\\n}"
  s="${s//$'\r'/\\r}"
  s="${s//$'\t'/\\t}"
  printf '%s' "$s"
}

printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"%s"}}\n' \
  "$(escape_for_json "$CONTEXT")"
