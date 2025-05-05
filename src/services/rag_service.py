"""
Thin wrapper around the existing query_rag() util in src.query.query_data
plus a helper to resolve user‑supplied policy IDs / names.
"""

from __future__ import annotations

import json
import pathlib
from functools import lru_cache
from typing import Optional

# Re‑use your working RAG pipeline
from src.query.query_data import query_rag as _query_rag, BASE_K

# ---------------------------------------------------------------------------
# Policy lookup helpers
# ---------------------------------------------------------------------------

_POLICY_MAP_PATH = pathlib.Path("data") / "policy_mapping.json"


@lru_cache(maxsize=1)
def _policy_mapping() -> dict[str, str]:
    """Load {policy_id: friendly_name} mapping once and cache it."""
    try:
        return json.loads(_POLICY_MAP_PATH.read_text())
    except FileNotFoundError:
        return {}


def find_policy(query: str) -> Optional[str]:
    """
    Return a canonical policy_id if *query* matches either an ID or a name;
    otherwise return None.
    """
    query = query.strip()
    if not query:
        return None

    mapping = _policy_mapping()

    # 1️⃣ Exact ID match
    if query in mapping:
        return query

    # 2️⃣ Friendly name → ID
    lowered = query.lower()
    for pid, name in mapping.items():
        if name.lower() == lowered:
            return pid

    return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def query_policy(question: str, policy_query: str, *, k: int = BASE_K) -> str:
    """
    High‑level helper:
    * figure out which policy index to hit
    * call the low‑level RAG pipeline
    """
    policy_id = find_policy(policy_query) or policy_query
    # If policy_id still unknown, _query_rag will likely throw – callers should
    # validate with `find_policy()` first when appropriate.
    return _query_rag(question, policy_id, k=k)
