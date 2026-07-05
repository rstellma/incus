#!/usr/bin/env python3

"""
Exports Incus state into declarative YAML spec.
"""
import yaml
from typing import List, Dict, Any

import incus as inc
import classify as cls
import repository as repo

def export_instance(name: str) -> None:
    """
    Export a single instance into spec/instances/.
    """

    data = inc.show_instance(name)

    profiles = data.get("profiles", [])
    ctype = cls.classify(profiles)

    path = repo.instance_path(name)

    spec = {
        "name": name,
        "type": ctype,
        "profiles": profiles,
        "config": data.get("config", {}),
        "devices": data.get("devices", {}),
    }

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        yaml.safe_dump(spec, f, sort_keys=False)


def export_all_instances() -> None:
    """
    Export all instances from Incus.
    """
    instances = inc.list_instances()

    for inst in instances:
        export_instance(inst["name"])


def export_profiles() -> None:
    """
    Export all profiles into spec/profiles/.
    """
    profiles = inc.list_profiles()

    for p in profiles:
        name = p["name"]

        path = repo.profile_path(name)

        spec = {
            "name": name,
            "config": p.get("config", {}),
            "devices": p.get("devices", {}),
        }

        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            yaml.safe_dump(spec, f, sort_keys=False)


def export_all() -> None:
    """
    Export full system state.
    """
    repo.ensure_structure()

    export_profiles()
    export_all_instances()
