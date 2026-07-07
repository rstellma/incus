#!/usr/bin/env python3

"""
Exports Incus state into declarative YAML spec.
"""
import yaml
from typing import List, Dict, Any
import re

import incus as inc
# import classify as cls
import repository as repo

def export_all_instances() -> None:
    """
    Export all instances from Incus.
    """
    instances = inc.list_instances()

    for inst in instances:
        export_instance(inst["name"])


def export_all_profiles() -> None:
    """
    Export all profiles from Incus.
    """
    profiles = inc.list_profiles()

    for prof in profiles:
        export_profile(prof["name"])


def export_all_networks() -> None:
    """
    Export all networks from Incus.
    """
    nets = inc.list_networks()

    for net in nets:
        if net["name"].startswith("incus"):
            export_network(net["name"])


def export_all_pools() -> None:
    """
    Export all storage pools from Incus.
    """
    pools = inc.list_pools()

    for pool in pools:
        export_pool(pool["name"])


def export_all_projects() -> None:
    """
    Export all storage pools from Incus.
    """
    projects = inc.list_projects()

    for p in projects:
        if p["name"] == "default":
          continue

        export_project(p["name"])


def export_instance(name: str) -> None:
    """
    Export a single instance into spec/instances/.
    """
    data = inc.show_instance(name)

    profiles = data.get("profiles", [])
#    ctype = cls.classify(profiles)

    path = repo.instance_path(name)
    config = data.get("config", {})

    image = "/".join([
        config.get("image.os", "").lower(),
        config.get("image.release", ""),
        config.get("image.variant", ""),
    ])

    spec = {
        "name": name,
#        "type": ctype,
        "profiles": profiles,
#        "config": image_config,
        "image": image
#        "devices": data.get("devices", {}),
    }

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        yaml.safe_dump(spec, f, sort_keys=False)


def export_profile(name: str) -> None:
    """
    Export a single profiles into spec/profiles/.
    """
    data = inc.show_profile(name)
    path = repo.profile_path(name)

    config = data.get("config", {})
    devices = data.get("devices",{})

    spec = {
        "name": name,
        "config": config,
        "devices": devices
    }

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        yaml.safe_dump(spec, f, sort_keys=False)


def export_network(name: str) -> None:
    """
    Export a single network into spec/profiles/.
    """
    data = inc.show_network(name)
    path = repo.network_path(name)

    config = data.get("config", {})
    typ = data.get("type", {})
    managed = data.get("managed", {})

    spec = {
        "name": name,
        "config": config,
        "type": typ,
        "managed": managed
    }

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        yaml.safe_dump(spec, f, sort_keys=False)


def export_pool(name: str) -> None:
    """
    Export a single storage pool  into spec/profiles/.
    """
    data = inc.show_pool(name)
    path = repo.storage_path(name)

    config = data.get("config", {})
    drvr = data.get("driver", {})

    spec = {
        "name": name,
        "config": config,
        "driver": drvr,
    }

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        yaml.safe_dump(spec, f, sort_keys=False)


def export_project(name: str) -> None:
    """
    Export a single project into spec/profiles/.
    """
    data = inc.show_project(name)
    path = repo.project_path(name)

    config = data.get("config", {})

    spec = {
        "name": name,
        "config": config,
    }

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        yaml.safe_dump(spec, f, sort_keys=False)


def export_all() -> None:
    """
    Export full system state.
    """
    repo.ensure_structure()

    export_all_instances()
    export_all_profiles()
    export_all_networks()
    export_all_pools()
    export_all_projects()
