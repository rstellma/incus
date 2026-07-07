#!/usr/bin/env python3

"""
Defines the filesystem layout of the declarative Incus system.
"""
from pathlib import Path
from typing import Optional

SPEC_ROOT = Path("spec")

def ensure_structure() -> None:
    (SPEC_ROOT / "profiles").mkdir(parents=True, exist_ok=True)
    (SPEC_ROOT / "instances").mkdir(parents=True, exist_ok=True)
    (SPEC_ROOT / "networks").mkdir(parents=True, exist_ok=True)
    (SPEC_ROOT / "storage").mkdir(parents=True, exist_ok=True)
    (SPEC_ROOT / "projects").mkdir(parents=True, exist_ok=True)

###
###     Instances
###
def instance_dir() -> Path:
    path = SPEC_ROOT / "instances"

    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")

    return path


def instance_path(name: str) -> Path:
    return instance_dir() / f"{name}.yaml"


def instance_specs() -> list[Path]:
    directory = instance_dir()

    files = sorted(directory.glob("*.yaml"))

    if not files:
        raise FileNotFoundError("No instance specifications found.")

    return files

###
###     Profiles
###
def profile_dir() -> Path:
    path = SPEC_ROOT / "profiles"

    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")

    return path


def profile_path(name: str) -> Path:
    return profile_dir() / f"{name}.yaml"


def profile_specs() -> list[Path]:
    profile = profile_dir()

    files = sorted(profile.glob("*.yaml"))

    if not files:
        raise FileNotFoundError("No profile specifications found.")

    return files

###
###     Networks
###
def network_dir() -> Path:
    path = SPEC_ROOT / "networks"

    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")

    return SPEC_ROOT / "networks"


def network_path(name: str) -> Path:
    return network_dir() / f"{name}.yaml"


def network_specs() -> list[Path]:
    network = network_dir()

    files = sorted(network.glob("*.yaml"))

    if not files:
        raise FileNotFoundError("No network specifications found.")

    return files

###
###     Storage Pools
###
def storage_dir() -> Path:
    path = SPEC_ROOT / "storage"

    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")

    return path


def storage_path(name: str) -> Path:
    return storage_dir() / f"{name}.yaml"


def storage_specs() -> list[Path]:
    storage = storage_dir()

    files = sorted(storage.glob("*.yaml"))

    if not files:
        raise FileNotFoundError("No storage specifications found.")

    return files

###
###     Projects
###
def project_dir() -> Path:
    path = SPEC_ROOT / "projects"

    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")

    return path


def project_path(name: str) -> Path:
    return project_dir() / f"{name}.yaml"


def project_specs() -> list[Path]:
    project = project_dir()

    files = sorted(project.glob("*.yaml"))

    if not files:
        raise FileNotFoundError("No project specifications found.")

    return files
