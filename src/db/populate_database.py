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
CHROMA_PATH = "chroma"
DATA_PATH = "data/policy_data"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)


def load_documents() -> list[Document]:
    loader = PyPDFDirectoryLoader(DATA_PATH)
    docs   = loader.load()

    if not docs:
        raise FileNotFoundError(
            f"No PDF documents found in {DATA_PATH!r}. "
            "Double‑check the path or add files before running."
        )

    return docs


def add_to_chroma(chunks: list[Document]):
    chunks_with_ids = calculate_chunk_ids(chunks)
    
    grouped: dict[str, list[Document]] = {}
    
    for c in chunks_with_ids:
        policy_id = Path(c.metadata["source"]).stem
        grouped.setdefault(policy_id, []).append(c)
    
    emb_fn = get_embedding()
    
    for policy_id, policy_chunks in grouped.items():
        db = Chroma(
                collection_name = policy_id,
            persist_directory = CHROMA_PATH,
            embedding_function = emb_fn,
        )

        existing_ids = set(db.get(include=[]).get("ids", []))
        new_chunks = [c for c in policy_chunks if c.metadata["id"] not in existing_ids]

        if new_chunks:
            print(f"👉 Adding {len(new_chunks)} chunks to collection '{policy_id}'")
            ids = [c.metadata["id"] for c in new_chunks]
            db.add_documents(new_chunks, ids=ids)
        else:
            print(f"✅ No new chunks for '{policy_id}'")


def calculate_chunk_ids(chunks: list[Document]):
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


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    load_dotenv()
    main()