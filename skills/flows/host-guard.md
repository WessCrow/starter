# Host Guard — modelo funcional

> Antes era só convenção textual em `AGENTS.md §0d`. Agora vira **execução real** via hook do harness.

---

## Modelo em duas camadas

| Camada | Responsabilidade | Onde vive |
|--------|------------------|-----------|
| **1. Convenção (soft)** | Texto em `AGENTS.md §0d` — diz ao agente o escopo permitido | `AGENTS.md` |
| **2. Hook (hard)** | Intercepta cada `Bash`/`run_command` *antes* de executar e bloqueia padrões perigosos | `skills/infra/scripts/host-guard.sh` + `.claude/settings.json` |

A camada 1 sozinha falha quando o agente alucina ou pula a regra. A camada 2 é determinística — exit 2 do hook impede a execução, independente do que o modelo decidir.

---

## O que o hook bloqueia (exit 2)

1. **Destrutivo massivo:** `rm -rf /`, `rm -rf ~`, `sudo rm`, `mkfs.*`, `dd if=…of=/dev/*`, fork bomb
2. **Pipe-to-shell:** `curl … | sh`, `wget … | bash` — código remoto sem revisão
3. **Paths sensíveis:** `/etc/passwd|shadow|sudoers`, `~/.ssh`, `~/.aws`, `/root/`
4. **Instalação global:** `npm/pnpm/yarn -g`, `sudo apt|brew|pip|npm` — STARTER opera local
5. **`cd` fora da raiz:** qualquer `cd /...` ou `cd ~` que escape de `$CLAUDE_PROJECT_DIR`
6. **Force push em `main`/`master`:** irreversível em branch protegida

Tudo o que **não** casa com esses padrões passa (exit 0). É um denylist focado, não allowlist exaustivo — para evitar fricção no fluxo normal de dev.

---

## Instalação (opt-in)

`.claude/settings.json` na raiz do projeto:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command",
            "command": "bash skills/infra/scripts/host-guard.sh" }
        ]
      }
    ]
  }
}
```

Para editores sem suporte a hooks (Antigravity, Windsurf): a camada 1 (texto em AGENTS.md) ainda vale — o agente é instruído a respeitar o escopo, mas sem garantia de runtime.

---

## Teste rápido

```bash
echo '{"tool_input":{"command":"rm -rf /"}}' | bash skills/infra/scripts/host-guard.sh
# → exit 2 + mensagem "destruição massiva do sistema"

echo '{"tool_input":{"command":"ls skills/"}}' | bash skills/infra/scripts/host-guard.sh
# → exit 0
```

---

## Evolução prevista

- **Allowlist por projeto:** ler `skills/core/runtime/host-guard.yaml` com paths/comandos extras permitidos
- **Modo audit:** logar em vez de bloquear, para calibrar padrões antes de fazer enforce
- **Integração CI:** rodar a mesma checagem em `.github/workflows/validate.yml` contra scripts commitados

---

> Autoria: Wesley Alves · Última atualização: 2026-06-13
