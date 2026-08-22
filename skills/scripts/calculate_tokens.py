#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
import datetime
from pathlib import Path

# Adiciona o diretório do script para imports relativos se houver
SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent
RUNTIME_DIR = WORKSPACE_ROOT / "skills" / "core" / "runtime"
HANDOFF_PATH = RUNTIME_DIR / "handoff.yaml"
TOKEN_LIMIT = 35000

def get_token_count(text: str) -> tuple[int, str]:
    try:
        import tiktoken
        # Usamos cl100k_base (padrão GPT-4 e Gemini)
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text)), "tiktoken (cl100k_base)"
    except ImportError:
        # Fallback matemático do STARTER: 1 token ≈ 4 caracteres
        if not text:
            return 0, "fallback (1 token ≈ 4 caracteres)"
        return max(1, len(text) // 4), "fallback (1 token ≈ 4 caracteres)"


def resolve_loaded_files(workspace_root: Path, raw_paths: list[str]) -> list[Path]:
    """Valida paths explícitos, restringe ao workspace e remove duplicatas."""
    if not raw_paths:
        raise ValueError("informe ao menos um arquivo efetivamente carregado")

    root = workspace_root.resolve()
    resolved: list[Path] = []
    for raw_path in raw_paths:
        candidate = Path(raw_path)
        path = (candidate if candidate.is_absolute() else root / candidate).resolve()
        try:
            path.relative_to(root)
        except ValueError as error:
            raise ValueError(f"arquivo fora do workspace: {raw_path}") from error
        if not path.is_file():
            raise ValueError(f"arquivo não encontrado: {raw_path}")
        if path not in resolved:
            resolved.append(path)
    return resolved


def build_context_metrics(
    workspace_root: Path,
    loaded_files: list[Path],
    date_value: str | None = None,
) -> dict:
    """Conta somente arquivos informados como carregados nesta sessão."""
    root = workspace_root.resolve()
    total_tokens = 0
    relative_paths: list[str] = []
    method_used = "fallback (1 token ≈ 4 caracteres)"

    for file_path in loaded_files:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        tokens, method_used = get_token_count(content)
        total_tokens += tokens
        relative_paths.append(str(file_path.relative_to(root)))

    return {
        "last_session_at": date_value or datetime.date.today().isoformat(),
        "files_loaded": relative_paths,
        "files_loaded_count": len(relative_paths),
        "estimated_tokens": total_tokens,
        "context_limit_exceeded": total_tokens > TOKEN_LIMIT,
        "unnecessary_files": [],
        "estimation_method": method_used,
    }

def main():
    parser = argparse.ArgumentParser(
        description="Conta tokens somente dos arquivos efetivamente carregados."
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Paths, dentro do workspace, carregados na sessão.",
    )
    args = parser.parse_args()

    try:
        import yaml
    except ImportError:
        print("Erro: biblioteca pyyaml não encontrada. Por favor, execute no ambiente virtual com as dependências.")
        sys.exit(1)

    if not HANDOFF_PATH.exists():
        print(f"Erro: {HANDOFF_PATH} não encontrado.")
        sys.exit(1)

    with open(HANDOFF_PATH, "r", encoding="utf-8") as f:
        handoff_data = yaml.safe_load(f) or {}

    try:
        loaded_files = resolve_loaded_files(WORKSPACE_ROOT, args.files)
    except ValueError as error:
        print(f"Erro: {error}")
        sys.exit(2)

    metrics = build_context_metrics(WORKSPACE_ROOT, loaded_files)

    handoff_data["context_metrics"] = metrics
    handoff_data["updated"] = datetime.date.today().isoformat()

    with open(HANDOFF_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(handoff_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(
        "Sucesso: handoff.yaml atualizado com "
        f"{metrics['files_loaded_count']} arquivos e {metrics['estimated_tokens']} tokens "
        f"usando {metrics['estimation_method']}"
    )
    
    if metrics["context_limit_exceeded"]:
        print(f"\n[AVISO DE CONTEXTO] Contexto estimado ({metrics['estimated_tokens']} tokens) excedeu o limite recomendado de {TOKEN_LIMIT} tokens.")
        print("Sugere-se executar a skill 'context-cleaner.skill' para arquivar/resumir arquivos desnecessários.")

if __name__ == "__main__":
    main()
