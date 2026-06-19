# Política de Segurança

## Versões com suporte

O STARTER é distribuído como um framework de arquivos (skills + `AGENTS.md`) copiado para dentro
de cada projeto. O suporte de segurança vale sempre para a **última versão `main`** publicada.

| Versão | Suporte           |
|--------|-------------------|
| 5.2.x  | ✅ ativa           |
| < 5.2  | ❌ atualize        |

## Como reportar uma vulnerabilidade

**Não abra uma issue pública** para falhas de segurança.

Use o canal privado do GitHub: aba **Security → Report a vulnerability**
(GitHub Private Vulnerability Reporting) em `https://github.com/WessCrow/starter`.

Ao reportar, inclua quando possível:
- descrição da falha e impacto potencial;
- passos para reproduzir (arquivo, skill ou script afetado);
- versão do framework e ambiente (editor/harness, SO).

**Resposta esperada:** confirmação de recebimento em até 5 dias úteis e um plano
de correção ou mitigação após a triagem inicial.

## Escopo

O STARTER inclui um **Host Guard** que bloqueia comandos perigosos e protege contra
vazamento de segredos locais (`.env`). Relatórios especialmente bem-vindos:
- bypass do Host Guard ou dos validadores (`validate.py`, `check-repo-hygiene.py`);
- scripts (`*.sh`) com injeção de comando ou path traversal;
- vazamento de segredos por convenções de runtime ou hooks de sessão.

Fora de escopo: vulnerabilidades em dependências de terceiros (reporte ao projeto de origem)
e em projetos gerados a partir do framework (responsabilidade do mantenedor do projeto filho).

---

> Parte do framework **STARTER** — criado e mantido por **Wesley Alves**.
