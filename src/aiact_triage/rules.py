"""Loads the rule set from the data directory.

The rules live in JSON, not in code, for two reasons: the legal content can
be reviewed without reading Python, and when the Digital Omnibus text is
published in the Official Journal the dates are corrected in one place.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"


@lru_cache(maxsize=None)
def _load(filename: str) -> dict:
    path = DATA_DIR / filename
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def timeline() -> dict[str, dict]:
    """Milestones keyed by id."""
    data = _load("timeline.json")
    return {m["id"]: m for m in data["milestones"]}


def timeline_meta() -> dict:
    return _load("timeline.json")["_meta"]


def prohibitions() -> dict[str, dict]:
    """Article 5 practices keyed by id."""
    data = _load("prohibitions.json")
    return {p["id"]: p for p in data["practices"]}


def annex_iii_areas() -> dict[str, dict]:
    data = _load("annex_iii.json")
    return {a["id"]: a for a in data["areas"]}


def art_6_3() -> dict:
    return _load("annex_iii.json")["art_6_3_derogation"]


def transparency_duties() -> list[dict]:
    return _load("transparency.json")["duties"]


def obligations() -> dict:
    return _load("obligations.json")


def cross_framework_rules() -> list[dict]:
    return _load("cross_framework.json")["rules"]
