#!/usr/bin/env python3

"""
Definition der grundlegenden Incus-Objekte.
Keine Logik, nur Struktur.
"""
from dataclasses import dataclass
from typing import Dict, List, Any


# ----------------------------
# Core Object Types
# ----------------------------

@dataclass
class Instance:
    name: str
    profiles: List[str]
    config: Dict[str, Any]
    devices: Dict[str, Any]


@dataclass
class Profile:
    name: str
    config: Dict[str, Any]
    devices: Dict[str, Any]


@dataclass
class Network:
    name: str
    config: Dict[str, Any]


@dataclass
class StoragePool:
    name: str
    driver: str
    config: Dict[str, Any]


@dataclass
class Project:
    name: str
    config: Dict[str, Any]
