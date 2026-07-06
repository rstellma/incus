import yaml
from pathlib import Path

import incus as inc
import repository as repo


#SPEC_DIR = Path("spec")
#INSTANCE_DIR = SPEC_DIR / "instances"

#INSTANCE = "instance"
#PROFILE = "profile"
#NETWORK = "network"
#POOL = "pool"
#PROJECT = "project"


# ---------------------------
# Helpers
# ---------------------------

def _read_yaml(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"YAML not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _instance_exists(name: str) -> bool:
    """
    Check if instance already exists in Incus.
    Uses YAML output only.
    """
    result = incus.run(["incus", "list", "--format=yaml"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    instances = yaml.safe_load(result.stdout) or []

    return any(i.get("name") == name for i in instances)


def _profile_exists(name: str) -> bool:
    """
    Check if profile already exists in Incus.
    Uses YAML output only.
    """
    result = incus.run(["incus", "profile", "list", "--format=yaml"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    profiles = yaml.safe_load(result.stdout) or []

    return any(p.get("name") == name for p in profiles)


def _network_exists(name: str) -> bool:
    """
    Check if network already exists in Incus.
    Uses YAML output only.
    """
    result = incus.run(["incus", "network", "list", "--format=yaml"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    networks = yaml.safe_load(result.stdout) or []

    return any(i.get("name") == name for i in networks)


def _storage_exists(name: str) -> bool:
    """
    Check if storage pool already exists in Incus.
    Uses YAML output only.
    """
    result = incus.run(["incus", "storage", "list", "--format=yaml"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    storage = yaml.safe_load(result.stdout) or []

    return any(i.get("name") == name for i in storage)


def _project_exists(name: str) -> bool:
    """
    Check if project already exists in Incus.
    Uses YAML output only.
    """
    result = incus.run(["incus", "project", "list", "--format=yaml"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    project = yaml.safe_load(result.stdout) or []

    return any(i.get("name") == name for i in project)


def _build_image(image_cfg: dict) -> str:
    """
    Reconstruct image string from YAML config.
    """
    os_name = image_cfg.get("image.os", "").lower()
    release = image_cfg.get("image.release", "")
    variant = image_cfg.get("image.variant", "")

    if not os_name or not release or not variant:
        raise ValueError(f"Incomplete image config: {image_cfg}")

    return f"{os_name}/{release}/{variant}"


# ---------------------------
# Public API
# ---------------------------

###
### Instances
###
def import_instance(name: str) -> None:
    """
    Import a single instance from YAML spec.
    """
    path = repo.instance_path(name)

    data = _read_yaml(path)

    yaml_name = data.get("name")
    if not yaml_name:
        raise ValueError(f"Missing 'name' in {path}")

    if yaml_name != name:
        raise ValueError(f"Name mismatch: file={yaml_name}, expected={name}")

    if _instance_exists(name):
        raise RuntimeError(f"Instance already exists: {name}")

    config = data.get("config", {})

    #image = _build_image(config)
    image = data.get("name", {})

    cmd = [
        "incus",
        "create",
        f"images:{image}",
        name,
    ]

    # YAML is piped into incus create
    result = incus.run_with_input(
        cmd,
        yaml.safe_dump(data, sort_keys=False),
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    print(f"[OK] imported instance: {name}")


def import_all_instances() -> None:
   for file in repo.instance_specs():
    import_instance(file.stem)

###
### Profiles
###
def import_profile(name: str) -> None:
    path = repo.profile_path(name)

    data = _read_yaml(path)

    if data.get("name") != name:
        raise ValueError(...)

    if _profile_exists(name):
        raise RuntimeError(f"Profile already exists: {name}")

    incus.run(["incus", "profile", "create", name])

    result = incus.run_with_input(
        ["incus", "profile", "edit", name],
        yaml.safe_dump(data, sort_keys=False),
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)


def import_all_profiles() -> None:
   for file in repo.profile_specs():
    import_profile(file.stem)

###
###     Networks
###
def import_network(name: str) -> None:
    path = repo.network_path(name)

    data = _read_yaml(path)

    if data.get("name") != name:
        raise ValueError(...)

    if _network_exists(name):
        raise RuntimeError(f"Network already exists: {name}")

    incus.run(["incus", "network", "create", name])

    result = incus.run_with_input(
        ["incus", "network", "edit", name],
        yaml.safe_dump(data, sort_keys=False),
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)


def import_all_networks() -> None:
   for file in repo.network_specs():
    import_network(file.stem)

###
###     Storage Pools
###
def import_storage(name: str) -> None:
    path = repo.storage_path(name)

    data = _read_yaml(path)

    if data.get("name") != name:
        raise ValueError(...)

    if _storage_exists(name):
        raise RuntimeError(f"Storage Pool already exists: {name}")

    incus.run(["incus", "storage", "create", name])

    result = incus.run_with_input(
        ["incus", "storage", "edit", name],
        yaml.safe_dump(data, sort_keys=False),
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)


def import_all_storage() -> None:
   for file in repo.storage_specs():
    import_storage(file.stem)

###
###     Projects
###
def import_project(name: str) -> None:
    path = repo.project_path(name)

    data = _read_yaml(path)

    if data.get("name") != name:
        raise ValueError(...)

    if _project_exists(name):
        raise RuntimeError(f"Project already exists: {name}")

    incus.run(["incus", "project", "create", name])

    result = incus.run_with_input(
        ["incus", "project", "edit", name],
        yaml.safe_dump(data, sort_keys=False),
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)


def import_all_projects() -> None:
   for file in repo.projects_specs():
    import_network(file.stem)


def import_all() -> None:
    """
    Import full system state.
    """

    import_all_instances()
    import_all_profiles()
    import_all_networks()
    import_all_pools()
    import_all_projects()
