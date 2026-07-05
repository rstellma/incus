#!/usr/bin/env python3

"""
Defines the filesystem layout of the declarative Incus system.
"""
from pathlib import Path
from typing import Optional

SPEC_ROOT = Path("spec")

def profile_path(name: str) -> Path:
    return SPEC_ROOT / "profiles" / f"{name}.yaml"


def instance_path(name: str) -> Path:
    return SPEC_ROOT / "instances" / f"{name}.yaml"


def network_path(name: str) -> Path:
    return SPEC_ROOT / "networks" / f"{name}.yaml"


def storage_path(name: str) -> Path:
    return SPEC_ROOT / "storage" / f"{name}.yaml"


def project_path(name: str) -> Path:
    return SPEC_ROOT / "projects" / f"{name}.yaml"


def ensure_structure() -> None:
    (SPEC_ROOT / "profiles").mkdir(parents=True, exist_ok=True)
    (SPEC_ROOT / "instances").mkdir(parents=True, exist_ok=True)
    (SPEC_ROOT / "networks").mkdir(parents=True, exist_ok=True)
    (SPEC_ROOT / "storage").mkdir(parents=True, exist_ok=True)
    (SPEC_ROOT / "projects").mkdir(parents=True, exist_ok=True)
