#!/usr/bin/env bash
# host-guard.sh — Hook PreToolUse:Bash do STARTER
#
# Lê o JSON do hook em stdin, extrai o campo command, e bloqueia
# (exit 2) padrões perigosos OU acesso fora da raiz do projeto.
#
# Instalação: registrar em .claude/settings.json:
#   "hooks": {
#     "PreToolUse": [{
#       "matcher": "Bash",
#       "hooks": [{ "type": "command",
#                   "command": "bash skills/infra/scripts/host-guard.sh" }]
#     }]
#   }
#
# Contratos do hook (Claude Code):
#   exit 0 → permitir
#   exit 2 → bloquear + stderr vira mensagem para o agente
#   outros → erro não-bloqueante

set -euo pipefail

# Raiz do projeto = CWD do agente (definida pelo harness).
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"

# Captura o JSON e extrai o comando (sem depender de jq).
INPUT="$(cat || true)"
CMD="$(printf '%s' "$INPUT" \
  | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
  | head -n1)"

[ -z "$CMD" ] && exit 0   # sem comando = nada a fazer

block() {
  echo "🚫 Host Guard: $1" >&2
  echo "   Comando: $CMD" >&2
  echo "   Motivo: $2" >&2
  exit 2
}

# ── 1. Comandos destrutivos sem caminho seguro ──────────────────────
case "$CMD" in
  *"rm -rf /"*|*"rm -rf /*"*|*"rm -rf ~"*|*"rm -rf \$HOME"*)
    block "rm -rf em raiz/home" "destruição massiva do sistema" ;;
  *"sudo rm "*|*"sudo dd "*|*"sudo mkfs"*)
    block "sudo destrutivo" "operação privilegiada perigosa" ;;
  *"mkfs."*|*"dd if="*"of=/dev/"*)
    block "formatação/escrita em device" "pode apagar discos" ;;
  *":(){ :|:& };:"*)
    block "fork bomb" "exaustão de processos" ;;
esac

# ── 2. Curl/wget pipe to shell ──────────────────────────────────────
if echo "$CMD" | grep -qE '(curl|wget)[^|]*\|[[:space:]]*(sh|bash|zsh)'; then
  block "pipe-to-shell" "executar script remoto sem revisão"
fi

# ── 3. Acesso a paths sensíveis fora do projeto ─────────────────────
SENSITIVE='(/etc/(passwd|shadow|sudoers)|~/\.ssh|\$HOME/\.ssh|~/\.aws|/root/|/var/root/)'
if echo "$CMD" | grep -qE "$SENSITIVE"; then
  block "acesso a path sensível" "fora do escopo do projeto (chaves/credenciais)"
fi

# ── 4. Instalação global de pacotes (use local sempre) ──────────────
if echo "$CMD" | grep -qE '(npm|pnpm|yarn)[[:space:]]+(i|install|add)[[:space:]]+-g\b'; then
  block "instalação global" "STARTER exige deps locais no projeto"
fi
if echo "$CMD" | grep -qE '\bsudo[[:space:]]+(apt|brew|pip|npm)\b'; then
  block "instalação global via sudo" "STARTER opera só na raiz do projeto"
fi

# ── 5. cd para fora da raiz do projeto ──────────────────────────────
if echo "$CMD" | grep -qE '^cd[[:space:]]+(/|~|\$HOME)'; then
  TARGET="$(echo "$CMD" | sed -nE 's/^cd[[:space:]]+([^[:space:];&|]+).*/\1/p')"
  case "$TARGET" in
    "$PROJECT_ROOT"*) ;;  # ok, ainda dentro
    *) block "cd fora da raiz" "agente restrito a $PROJECT_ROOT" ;;
  esac
fi

# ── 6. Git destrutivo sem confirmação explícita ─────────────────────
if echo "$CMD" | grep -qE 'git[[:space:]]+push[[:space:]]+.*--force\b' \
   && ! echo "$CMD" | grep -q 'origin[[:space:]]\+main\|master'; then
  : # force push em branch de feature é tolerado
elif echo "$CMD" | grep -qE 'git[[:space:]]+push[[:space:]]+.*--force.*\b(main|master)\b'; then
  block "force push em main/master" "operação irreversível em branch protegida"
fi

exit 0
