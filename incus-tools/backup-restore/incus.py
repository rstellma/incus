#!/usr/bin/env python3

"""
Low-level interface to Incus.
Only this module is allowed to call the incus CLI.
"""
import subprocess
import json
from typing import List, Dict, Any, Optional
import yaml

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


# 3. Profile Listing
def list_profiles() -> List[Dict[str, Any]]:
    #result = run(["incus", "profile", "list", "--format=json"])
    result = run(["incus", "profile", "list"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return json.loads(result.stdout)


# 4. Network Listing
def list_networks() -> List[Dict[str, Any]]:
    result = run(["incus", "network", "list"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return json.loads(result.stdout)


# 5. Storage Listing
def list_storage() -> List[Dict[str, Any]]:
    result = run(["incus", "storage", "list"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return json.loads(result.stdout)


# 6. Project Listing
def list_storage() -> List[Dict[str, Any]]:
    result = run(["incus", "project", "list"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return json.loads(result.stdout)


# 7. Single Instance Details
def show_instance(name: str) -> Dict[str, Any]:
    """
    Returns full instance config (YAML from Incus parsed as dict).
    """
    result = run(["incus", "config", "show", name])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    # Incus returns YAML → Python needs YAML parser later
    # -> pip3 install pyyaml
    #import yaml

    return yaml.safe_load(result.stdout)


# 8. Single Profile Details
def show_profile(name: str) -> Dict[str, Any]:
    """
    Returns full profile config (YAML from Incus parsed as dict).
    """
    result = run(["incus", "profile", "show", name])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return yaml.safe_load(result.stdout)


# 9. Single Profile Details
def show_network(name: str) -> Dict[str, Any]:
    """
    Returns full network config (YAML from Incus parsed as dict).
    """
    result = run(["incus", "network", "show", name])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return yaml.safe_load(result.stdout)


# 10. Single Stortage Pool Details
def show_storage(name: str) -> Dict[str, Any]:
    """
    Returns full storage pool  config (YAML from Incus parsed as dict).
    """
    result = run(["incus", "storage", "show", name])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return yaml.safe_load(result.stdout)


# 11. Single Project Details
def show_project(name: str) -> Dict[str, Any]:
    """
    Returns full project config (YAML from Incus parsed as dict).
    """
    result = run(["incus", "project", "show", name])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return yaml.safe_load(result.stdout)
