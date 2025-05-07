"""
Thin wrapper around the existing query_rag() util in src.query.query_data
plus a helper to resolve user‑supplied policy IDs / names.
"""

from __future__ import annotations

import json
import pathlib
from functools import lru_cache
from typing import Optional

from langchain_chroma import Chroma
from src.ingest.embedding_creator import get_embedding
from src.services.openai_service import ask_openai
import os

# Re‑use your working RAG pipeline
from src.query.query_data import query_rag as _query_rag, BASE_K

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

    if query in mapping:
        return query

    lowered = query.lower()
    for pid, name in mapping.items():
        if name.lower() == lowered:
            return pid

    return None


def query_policy(question: str, policy_query: str, *, k: int = BASE_K) -> str:
    """
    High‑level helper:
    * figure out which policy index to hit
    * call the low‑level RAG pipeline
    """
    policy_id = find_policy(policy_query) or policy_query

    q_lower = question.lower().strip()
    if "summarize" in q_lower or "summary" in q_lower:
        return summarize_policy(policy_id)
    return _query_rag(question, policy_id, k=k)

SUMMARY_PROMPT = """\
You are a helpful assistant. The user has requested a summary of their insurance policy below.

Policy Document:
\"\"\"
{policy_content}
\"\"\"

Please provide a concise and comprehensive summary of this policy, highlighting the main coverage, benefits, and important conditions.
"""

def summarize_policy(policy_id: str) -> str:
    """
    Retrieve *all* chunks for the given policy and ask the LLM to summarize them.
    """
    db = Chroma(
        collection_name=policy_id,
        persist_directory=os.getenv("CHROMA_DB_DIR", "chroma"),
        embedding_function=get_embedding()
    )
    all_data = db.get()
    chunks = all_data.get("documents", [])
    full_text = "\n\n".join(chunks)
    prompt = SUMMARY_PROMPT.format(policy_content=full_text)
    return ask_openai(prompt)
