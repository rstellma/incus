#!/usr/bin/env python3

"""
Low-level interface to Incus.
Only this module is allowed to call the incus CLI.
"""
import subprocess
import json
from typing import List, Dict, Any, Optional
import yaml


def object_exists(obj_type: str, name: str) -> bool:
    """
    Check whether an Incus object exists.

    Supported object types:
        instance
        profile
        network
        pool
        project
    """

    commands = {
        "instance": ["incus", "list", "--format=yaml"],
        "profile":  ["incus", "profile", "list", "--format=yaml"],
        "network":  ["incus", "network", "list", "--format=yaml"],
        "pool":     ["incus", "storage", "list", "--format=yaml"],
        "project":  ["incus", "project", "list", "--format=yaml"],
    }

    if obj_type not in commands:
        raise ValueError(f"Unsupported object type: {obj_type}")

    result = run(commands[obj_type])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    objects = yaml.safe_load(result.stdout) or []

    return any(obj.get("name") == name for obj in objects)


# 1. Core Runner
def run(
    cmd: List[str],
    stdin: TextIO | None = None,
) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        stdin=stdin,
        capture_output=True,
        text=True,
        check=False,
    )

def run_with_input(cmd: List[str], stdin: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        input=stdin,
        capture_output=True,
        text=True,
        check=False,
    )

# 2. Instance List
def list_instances() -> List[Dict[str, Any]]:
    """
    Returns raw Incus JSON instance list.
    """
    # result = run(["incus", "list", "--format=json"])
    result = run(["incus", "list", "--format=yaml"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    # return json.loads(result.stdout)
    return yaml.safe_load(result.stdout)


# 3. Profile Listing
def list_profiles() -> List[Dict[str, Any]]:
    # result = run(["incus", "profile", "list", "--format=json"])
    result = run(["incus", "profile", "list", "--format=yaml"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    # return json.loads(result.stdout)
    return yaml.safe_load(result.stdout)


# 4. Network Listing
def list_networks() -> List[Dict[str, Any]]:
    result = run(["incus", "network", "list", "--format=yaml"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    # return json.loads(result.stdout)
    return yaml.safe_load(result.stdout)


# 5. Storage Listing
def list_pools() -> List[Dict[str, Any]]:
    result = run(["incus", "storage", "list", "--format=yaml"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    # return json.loads(result.stdout)
    return yaml.safe_load(result.stdout)


# 6. Project Listing
def list_projects() -> List[Dict[str, Any]]:
    result = run(["incus", "project", "list", "--format=yaml"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    # return json.loads(result.stdout)
    return yaml.safe_load(result.stdout)


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


# 9. Single Network Details
def show_network(name: str) -> Dict[str, Any]:
    """
    Returns full network config (YAML from Incus parsed as dict).
    """
    result = run(["incus", "network", "show", name])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return yaml.safe_load(result.stdout)


# 10. Single Stortage Pool Details
def show_pool(name: str) -> Dict[str, Any]:
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
