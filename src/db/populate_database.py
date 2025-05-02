import argparse
import os
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed

from dotenv import load_dotenv
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader

from src.ingest.embedding_creator import get_embedding
from src.ingest.split_pds import split_documents

CHROMA_PATH = "chroma"
DATA_PATH = "data"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    documents = load_documents()
    chunks = split_documents(
            documents,
            chunk_size = int(os.getenv("CHUNK_SIZE", "800")),
        chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "80")),
    )
    
    # === EMBEDDING IN PARALLEL ===
    # instead of embedding one-by-one, fire off a pool of workers
    def embed_chunk(chunk):
        chunk.metadata["embedding"] = get_embedding()(chunk.page_content)
        return chunk
    
    
    with ProcessPoolExecutor() as pool:
        futures = [pool.submit(embed_chunk, c) for c in chunks]
        chunks = [f.result() for f in as_completed(futures)]
    

    add_to_chroma(chunks)


def load_documents():
    loader = PyPDFDirectoryLoader(DATA_PATH)
    return loader.load()


def add_to_chroma(chunks: list[Document]):
    # instantiate (auto-persisting) Chroma
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding(),
    )

    # tag each chunk with a stable ID
    chunks_with_ids = calculate_chunk_ids(chunks)

    # find what’s already in the DB
    existing = db.get(include=[])  # will always include “ids”
    existing_ids = set(existing.get("ids", []))
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # filter out chunks we’ve already stored
    new_chunks = [c for c in chunks_with_ids if c.metadata["id"] not in existing_ids]

    if new_chunks:
        print(f"👉 Adding new documents: {len(new_chunks)}")
        ids = [c.metadata["id"] for c in new_chunks]
        db.add_documents(new_chunks, ids=ids)
        # no db.persist() needed—Chroma auto-persists now
    else:
        print("✅ No new documents to add")


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
