#!/usr/bin/env python3

"""
Semantic classification based on profiles.
"""
from typing import List, Optional

PROFILE_RULES = [
    ("10-Env_Desktop", "Desktop"),
    ("20-Apps_", "App (Internet)"),
    ("21-Apps_", "App (Offline)"),
    ("22-Apps_", "Leisure"),
    ("30-Dev_", "Development"),
]

def classify(profiles: List[str]) -> Optional[str]:
    """
    Classify an instance based on its profiles.

    Returns:
        "desktop"
        "app"
        "development"
        None -> unknown / ignore
    """
    for prefix, kind in PROFILE_RULES:

        # exact match
        if prefix.endswith("_") is False:
            if prefix in profiles:
                return kind
        # prefix match
        else:
            if any(p.startswith(prefix) for p in profiles):
                return kind

    return None
