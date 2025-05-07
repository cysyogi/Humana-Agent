# src/db/populate_database.py
import argparse
import os
import shutil
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.schema import Document

from src.ingest.embedding_creator import get_embedding
from src.ingest.split_pds import split_documents
from langchain_chroma import Chroma

CHROMA_PATH = os.getenv("CHROMA_DB_DIR", "chroma")
DATA_PATH = os.getenv("POLICY_DATA_DIR", "data/policy_data")


def clear_database():
    """Completely remove the existing Chroma DB."""
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


def load_documents() -> list[Document]:
    """Load all PDFs under DATA_PATH."""
    loader = PyPDFDirectoryLoader(DATA_PATH)
    docs = loader.load()
    if not docs:
        raise FileNotFoundError(
            f"No PDF documents found in {DATA_PATH!r}. "
            "Add files before running."
        )
    else:
        print("Found %d PDFs." % len(docs))
    return docs


def calculate_chunk_ids(chunks: list[Document]) -> list[Document]:
    """
    Assign a unique metadata['id'] to each chunk based on source file & page.
    """
    last_page_id = None
    idx = 0
    for c in chunks:
        src = c.metadata.get("source")
        page = c.metadata.get("page")
        page_id = f"{src}:{page}"
        if page_id == last_page_id:
            idx += 1
        else:
            idx = 0
            last_page_id = page_id
        c.metadata["id"] = f"{page_id}:{idx}"
    return chunks


def add_to_chroma(chunks: list[Document]):
    """
    Group chunks by policy_id (filename stem) and add only the *new* ones to Chroma.
    """
    chunks_with_ids = calculate_chunk_ids(chunks)
    grouped: dict[str, list[Document]] = {}
    for c in chunks_with_ids:
        policy_id = Path(c.metadata["source"]).stem
        grouped.setdefault(policy_id, []).append(c)

    emb_fn = get_embedding()
    for policy_id, policy_chunks in grouped.items():
        db = Chroma(
            collection_name=policy_id,
            persist_directory=CHROMA_PATH,
            embedding_function=emb_fn,
        )
        # fetch existing IDs so we don't re-add
        existing_ids = set(db.get(include=[]).get("ids", []))
        new_chunks = [
            c for c in policy_chunks if c.metadata["id"] not in existing_ids
        ]
        if new_chunks:
            print(f"👉 Adding {len(new_chunks)} new chunks to '{policy_id}'")
            ids = [c.metadata["id"] for c in new_chunks]
            db.add_documents(new_chunks, ids=ids)
        else:
            print(f"✅ No new chunks for '{policy_id}'")


def ingest_policies(reset: bool = False):
    """
    Incrementally ingest all PDFs under DATA_PATH.

    Args:
      reset: if True, clear the entire DB first (like --reset).
    """
    if reset:
        print("✨ Clearing existing Chroma DB…")
        clear_database()
    docs = load_documents()
    chunks = split_documents(docs)
    add_to_chroma(chunks)


def main():
    """CLI entrypoint. Use --reset to force a full reindex."""
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reset", action="store_true", help="Clear DB before ingesting"
    )
    args = parser.parse_args()
    ingest_policies(reset=args.reset)


if __name__ == "__main__":
    main()