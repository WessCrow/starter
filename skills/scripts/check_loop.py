#!/usr/bin/env python3
"""
STARTER check_loop.py — Detecta loops repetitivos de chamadas de ferramentas.
Inspirado no LoopDetectionMiddleware do ByteDance DeerFlow 2.0.
"""
from __future__ import annotations
import sys
import json
import hashlib
from pathlib import Path
from typing import Optional, Tuple, List, Dict

# Configurações padrão
DEFAULT_WARN_THRESHOLD = 3
DEFAULT_HARD_LIMIT = 5

def hash_tool_call(name: str, args: dict) -> str:
    """Gera um hash determinístico da chamada de ferramenta."""
    # Normalização de argumentos
    arg_str = json.dumps(args, sort_keys=True, default=str)
    blob = f"{name}:{arg_str}"
    return hashlib.md5(blob.encode("utf-8")).hexdigest()[:12]

def find_latest_transcript(app_data_dir: Path) -> Optional[Path]:
    """Varre a pasta brain para encontrar o transcript.jsonl ativo mais recente."""
    brain_dir = app_data_dir / "brain"
    if not brain_dir.exists():
        return None
    
    transcripts = []
    for conv_dir in brain_dir.iterdir():
        if conv_dir.is_dir():
            t_file = conv_dir / ".system_generated" / "logs" / "transcript.jsonl"
            if t_file.exists():
                transcripts.append(t_file)
                
    if not transcripts:
        return None
        
    # Ordena pelo tempo de modificação
    return max(transcripts, key=lambda p: p.stat().st_mtime)

def analyze_transcript(transcript_path: Path, warn_thresh: int, hard_lim: int) -> Tuple[str, str]:
    """Analisa o arquivo transcript.jsonl em busca de loops."""
    if not transcript_path.exists():
        return "PASS", f"Arquivo de logs não encontrado: {transcript_path}"

    tool_call_history = []
    
    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                line_str = line.strip()
                if not line_str:
                    continue
                step = json.loads(line_str)
                # Verifica se há chamadas de ferramenta registradas
                tool_calls = step.get("tool_calls") or []
                for tc in tool_calls:
                    name = tc.get("name") or tc.get("ToolName")
                    args = tc.get("Arguments") or tc.get("args") or {}
                    if name:
                        h = hash_tool_call(name, args)
                        tool_call_history.append((name, h))
            except Exception:
                continue

    if not tool_call_history:
        return "PASS", "Nenhuma chamada de ferramenta registrada ainda."

    # Analisar a janela recente (últimas 10 chamadas de ferramentas)
    recent_calls = tool_call_history[-10:]
    hashes = [h for _, h in recent_calls]
    
    for (name, h) in set(recent_calls):
        count = hashes.count(h)
        if count >= hard_lim:
            return "FAIL", f"A ferramenta '{name}' foi chamada repetidamente {count} vezes com os mesmos argumentos. Abortando para quebrar o loop."
        elif count >= warn_thresh:
            return "WARN", f"Atenção: A ferramenta '{name}' está se repetindo ({count} vezes)."
            
    return "PASS", f"Padrão de execução saudável ({len(tool_call_history)} chamadas registradas)."

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Verificador de loops do STARTER")
    parser.add_argument("--transcript", type=str, help="Caminho direto para o transcript.jsonl")
    parser.add_argument("--warn", type=int, default=DEFAULT_WARN_THRESHOLD, help="Limite para avisos")
    parser.add_argument("--hard", type=int, default=DEFAULT_HARD_LIMIT, help="Limite rígido para falha")
    parser.add_argument("--app-data", type=str, default="/Users/drt79427/.gemini/antigravity-ide", help="Caminho do App Data do Gemini")
    
    args = parser.parse_args()
    
    if args.transcript:
        transcript_path = Path(args.transcript)
    else:
        app_data_path = Path(args.app_data)
        transcript_path = find_latest_transcript(app_data_path)
        if not transcript_path:
            print("STATUS: PASS - Não foi possível autodetectar nenhum transcript.jsonl")
            sys.exit(0)
            
    status, msg = analyze_transcript(transcript_path, args.warn, args.hard)
    print(f"STATUS: {status} - {msg}")
    
    if status == "FAIL":
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
