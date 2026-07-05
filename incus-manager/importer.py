#!/usr/bin/env python3

"""
Imports declarative YAML spec into Incus.
"""
import yaml
from typing import Dict, Any

import incus as inc
import repository as repo

def import_instance(name: str) -> None:
    """
    Apply spec/instances/<name>.yaml to Incus.
    """
    path = repo.instance_path(name)

    if not path.exists():
        raise FileNotFoundError(f"No spec for instance: {name}")

    with open(path) as f:
        spec = yaml.safe_load(f)

    # --- Minimal invasive approach ---
    # (wir starten bewusst NICHT mit full recreate!)
    existing = inc.list_instances()
    existing_names = [i["name"] for i in existing]

    if name not in existing_names:
        print(f"[IMPORT] Instance {name} does not exist yet → skipping creation logic (TBD)")
        return

    # TODO: später:
    # - config compare
    # - profile reconciliation
    # - device reconciliation

    print(f"[IMPORT] Instance {name} loaded (no-op for now)")


def import_all_instances() -> None:
    """
    Import all instances from spec.
    """
    instances_dir = repo.SPEC_ROOT / "instances"

    if not instances_dir.exists():
        raise FileNotFoundError("No instances directory in spec")

    for file in instances_dir.glob("*.yaml"):
        import_instance(file.stem)


def import_profiles() -> None:
    """
    Profiles are intentionally not fully applied yet.
    """
    profiles_dir = repo.SPEC_ROOT / "profiles"

    if not profiles_dir.exists():
        return

    for file in profiles_dir.glob("*.yaml"):
        print(f"[IMPORT] Profile {file.stem} (TBD)")


def import_all() -> None:
    """
    Full system import (safe mode).
    """
    import_profiles()
    import_all_instances()
