#!/usr/bin/env python3
"""
STARTER Session Recorder — v1.0.0
Records session metadata, files touched, and git status into a trace file in qa/runs/.
"""
from __future__ import annotations

import os
import json
import datetime
import subprocess
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parents[3]
RUNTIME_DIR = REPO_ROOT / "skills" / "core" / "runtime"
RUNS_DIR = REPO_ROOT / "qa" / "runs"

def load_yaml(path: Path) -> dict:
    """Helper to load a YAML file simply."""
    if not path.exists():
        return {}
    try:
        import yaml
        with path.open(encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        # Simple parser fallback
        data = {}
        with path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    k, v = line.split(":", 1)
                    data[k.strip()] = v.strip().strip('"').strip("'")
        return data

def run_cmd(args: list[str]) -> str:
    """Runs a shell command and returns output."""
    try:
        res = subprocess.run(args, cwd=REPO_ROOT, capture_output=True, text=True, check=False)
        return res.stdout.strip()
    except Exception:
        return ""

def main():
    print("--- INICIANDO RECORD SESSION (LOOP 1) ---")
    
    # Ensure runs directory exists
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load Handoff and State
    handoff = load_yaml(RUNTIME_DIR / "handoff.yaml")
    state = load_yaml(RUNTIME_DIR / "state.yaml")
    
    feature_id = handoff.get("feature", {}).get("id", "sprint-indefinida")
    if not isinstance(feature_id, str):
        feature_id = "sprint-indefinida"
        
    last_completed = handoff.get("session", {}).get("last_completed", "")
    
    # Capture Git details
    git_status = run_cmd(["git", "status", "--porcelain"])
    git_diff_names = run_cmd(["git", "diff", "--name-only", "HEAD"])
    files_touched = [f.strip() for f in git_diff_names.splitlines() if f.strip()]
    
    # Trace structure
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    trace = {
        "timestamp": timestamp,
        "feature_id": feature_id,
        "last_completed": last_completed,
        "git_status_raw": git_status,
        "files_touched": files_touched,
        "framework_version": state.get("framework_v", "unknown"),
        "qa_status": handoff.get("qa", {}).get("last_status", "unknown")
    }
    
    # File name based on timestamp and feature
    safe_feature = "".join(c for c in feature_id if c.isalnum() or c in ("-", "_"))
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    trace_file = RUNS_DIR / f"session_{date_str}_{safe_feature}.json"
    
    with trace_file.open("w", encoding="utf-8") as f:
        json.dump(trace, f, indent=2, ensure_ascii=False)
        
    print(f"Trace de sessão registrado com sucesso: {trace_file.relative_to(REPO_ROOT)}")

if __name__ == "__main__":
    main()
