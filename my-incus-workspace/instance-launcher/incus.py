#!/usr/bin/env python3

"""
Low-level interface to Incus.
Only this module is allowed to call the incus CLI.
"""
import subprocess
import json
from typing import List, Dict, Any, Optional

# 1. Core Runner
def run(cmd: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )

# 2. Instance List
def list_instances() -> List[Dict[str, Any]]:
    """
    Returns raw Incus JSON instance list.
    """
    result = run(["incus", "list", "--format=json"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return json.loads(result.stdout)


# 3. Single Instance Details
def show_instance(name: str) -> Dict[str, Any]:
    """
    Returns full instance config (YAML from Incus parsed as dict).
    """
    result = run(["incus", "config", "show", name])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    # Incus returns YAML → Python needs YAML parser later
    # -> pip3 install pyyaml
    import yaml

    return yaml.safe_load(result.stdout)


# 4. Instance Lifecycle
def start_instance(name: str) -> None:
    result = run(["incus", "start", name])
    if result.returncode != 0:
        raise RuntimeError(result.stderr)


def stop_instance(name: str) -> None:
    result = run(["incus", "stop", name])
    if result.returncode != 0:
        raise RuntimeError(result.stderr)

"""
# 5. Profile Listing
def list_profiles() -> List[Dict[str, Any]]:
    result = run(["incus", "profile", "list", "--format=json"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return json.loads(result.stdout)
"""
