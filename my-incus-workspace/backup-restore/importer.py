import yaml
from pathlib import Path

import incus as inc
import repository as repo


#SPEC_DIR = Path("spec")
#INSTANCE_DIR = SPEC_DIR / "instances"




# ---------------------------
# Helpers
# ---------------------------

def _read_yaml(path: Path) -> dict:
    print("_read_yaml")
    if not path.exists():
        raise FileNotFoundError(f"YAML not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _instance_exists(name: str) -> bool:
    print("_instance_exists")
    """
    Check if instance already exists in Incus.
    Uses YAML output only.
    """
    result = inc.run(["incus", "list", "--format=yaml"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    instances = yaml.safe_load(result.stdout) or []

    return any(i.get("name") == name for i in instances)


def _profile_exists(name: str) -> bool:
    print("_profile_exists")
    """
    Check if profile already exists in Incus.
    Uses YAML output only.
    """
    result = inc.run(["incus", "profile", "list", "--format=yaml"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    profiles = yaml.safe_load(result.stdout) or []

    return any(p.get("name") == name for p in profiles)


def _network_exists(name: str) -> bool:
    print("_network_exists")
    """
    Check if network already exists in Incus.
    Uses YAML output only.
    """
    result = inc.run(["incus", "network", "list", "--format=yaml"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    networks = yaml.safe_load(result.stdout) or []

    return any(i.get("name") == name for i in networks)


def _storage_exists(name: str) -> bool:
    print("_storage_exists")
    """
    Check if storage pool already exists in Incus.
    Uses YAML output only.
    """
    result = inc.run(["incus", "storage", "list", "--format=yaml"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    storage = yaml.safe_load(result.stdout) or []

    return any(i.get("name") == name for i in storage)


def _project_exists(name: str) -> bool:
    print("_project_exists")
    """
    Check if project already exists in Incus.
    Uses YAML output only.
    """
    result = inc.run(["incus", "project", "list", "--format=yaml"])

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    project = yaml.safe_load(result.stdout) or []

    return any(i.get("name") == name for i in project)


def _build_image(image_cfg: dict) -> str:
    print("_build_image")
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
def import_all() -> None:
    """
    Import full system state.
    """
    import_all_projects()
    import_all_storage()
    import_all_networks()
    import_all_profiles()
    import_all_instances()


###
### Instances
###
def import_instance(name: str) -> None:
    print("import_instance")
    """
    Import a single instance from YAML spec.
    """
    path = repo.instance_path(name)

    data = _read_yaml(path)

    if data["name"] != name:
        raise ValueError(f"Instance has wrong name: {name}, expected: {data["name"]}")

    if inc.object_exists(inc.INSTANCE, name):
        raise RuntimeError(f"Instance already exists: {name}")

    image = data["image"]

    with open(path, encoding="utf-8") as f:
        result = inc.run(
            ["incus", "create", f"images:{image}", name],
            stdin=f,
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
    print("import_profile")
    path = repo.profile_path(name)

    data = _read_yaml(path)

    if data["name"] != name:
        raise ValueError(f"Profile has wrong name: {name}, expected: {data["name"]}")

    if inc.object_exists(inc.PROFILE, name):
        raise RuntimeError(f"Profile already exists: {name}")

    with open(path, encoding="utf-8") as f:
        result = inc.run(
            ["incus", "profile", "create", name],
            stdin=f,
        )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    print(f"[OK] imported profile: {name}")


def import_all_profiles() -> None:
   for file in repo.profile_specs():
    import_profile(file.stem)

###
###     Networks
###
def import_network(name: str) -> None:
    print("import_network")
    path = repo.network_path(name)

    data = _read_yaml(path)

    if data["name"] != name:
        raise ValueError(f"Network has wrong name: {name}, expected: {data["name"]}")

    if inc.object_exists(inc.NETWORK, name):
        raise RuntimeError(f"Profile already exists: {name}")

    with open(path, encoding="utf-8") as f:
        result = inc.run(
            ["incus", "network", "create", name],
            stdin=f,
        )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    print(f"[OK] imported network: {name}")


def import_all_networks() -> None:
   for file in repo.network_specs():
    import_network(file.stem)

###
###     Storage Pools
###
def import_storage(name: str) -> None:
    print("import_storage")
    path = repo.storage_path(name)
    print(path)

    data = _read_yaml(path)

    driver = data.get("driver")
    source = data.get("config")
    print(source["source"])

    Path(source["source"]).mkdir(parents=True, exist_ok=True)

    if data.get("name") != name:
        raise ValueError(f"Storage Pool has wrong name: {name}, expected: {data["name"]}")

    if inc.object_exists(inc.STORAGE, name):
        raise RuntimeError(f"Storage Pool already exists: {name}")

    with open(path, encoding="utf-8") as f:
        result = inc.run(
            ["incus", "storage", "create", name, driver],
            stdin=f,
        )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    print(f"[OK] imported storage pool: {name}")


def import_all_storage() -> None:
   for file in repo.storage_specs():
    import_storage(file.stem)

###
###     Projects
###
def import_project(name: str) -> None:
    print("import_project")
    path = repo.project_path(name)

    data = _read_yaml(path)

    if data.get("name") != name:
        raise ValueError(f"Project has wrong name: {name}, expected: {data["name"]}")

    if inc.object_exists(inc.PROJECT, name):
        raise RuntimeError(f"Project already exists: {name}")

    with open(path, encoding="utf-8") as f:
        result = inc.run(
            ["incus", "storage", "create", name],
            stdin=f,
        )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    print(f"[OK] imported project: {name}")


def import_all_projects() -> None:
   for file in repo.project_specs():
    import_project(file.stem)
