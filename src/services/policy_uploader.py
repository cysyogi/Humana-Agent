# src/services/policy_uploader.py

import json
import logging
from pathlib import Path

from fastapi import UploadFile

from src.db.populate_database import ingest_policies

# Configurable directories & files
UPLOAD_DIR = Path("data/policy_data")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAPPING_FILE = Path("data/policy_mapping.json")


async def save_policy_pdf(file: UploadFile) -> str:
    """
    Persist the uploaded PDF to disk. Returns the policy_id (filename without .pdf).
    """
    if file.content_type != "application/pdf":
        raise ValueError("Only PDF files are supported.")
    contents = await file.read()
    saved_path = UPLOAD_DIR / file.filename
    saved_path.write_bytes(contents)
    logging.info(f"[PolicyUploader] Saved PDF to {saved_path}")
    return saved_path.stem  # policy_id


def update_policy_mapping(policy_id: str, friendly_name: str) -> None:
    """
    Ensure data/policy_mapping.json maps this policy_id to the given friendly name.
    """
    mapping = {}
    if MAPPING_FILE.exists():
        mapping = json.loads(MAPPING_FILE.read_text())

    # Override or set the mapping entry to the user‑provided friendly_name
    mapping[policy_id] = friendly_name
    MAPPING_FILE.write_text(json.dumps(mapping, indent=2))
    logging.info(f"[PolicyUploader] Updated mapping: {policy_id} -> {friendly_name}")


def ingest_all_policies() -> None:
    """
    Trigger the ingestion pipeline to (re)index all PDFs under data/.
    """
    logging.info("[PolicyUploader] Starting incremental ingestion…")
    ingest_policies(reset=False)
    logging.info("[PolicyUploader] Incremental ingestion complete.")
