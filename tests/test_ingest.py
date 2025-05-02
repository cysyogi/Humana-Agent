from pathlib import Path
from pypdf import PdfWriter
import pytest
from src.ingest.load_pfds import load_document
from src.ingest.split_pds import (
    split_documents,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)
from langchain.schema import Document


@pytest.fixture
def dummy_pdf_dir(tmp_path: Path) -> Path:
    """
    Create a temporary directory with one tiny blank PDF.
    """
    pdf_path = tmp_path / "dummy.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=595, height=842)  # A4 size
    with open(pdf_path, "wb") as f:
        writer.write(f)
    return tmp_path


def test_load_document_returns_document_list(dummy_pdf_dir: Path):
    docs = load_document(str(dummy_pdf_dir))
    # must be a list
    assert isinstance(docs, list)
    # one PDF → one Document
    assert len(docs) == 1

    doc = docs[0]
    # Document has page_content and metadata.source pointing at our file
    assert hasattr(doc, "page_content")
    assert isinstance(doc.page_content, str)
    assert doc.metadata.get("source", "").endswith("dummy.pdf")


def test_split_documents_respects_constants():
    # create one Document whose content is 1.5× CHUNK_SIZE
    total_length = CHUNK_SIZE + CHUNK_SIZE // 2
    content = "A" * total_length
    doc = Document(page_content=content, metadata={"id": "test"})

    chunks = split_documents([doc])
    # we expect at least two chunks
    assert len(chunks) >= 2

    # first chunk is exactly CHUNK_SIZE
    assert len(chunks[0].page_content) == CHUNK_SIZE

    # no chunk exceeds CHUNK_SIZE
    assert all(len(c.page_content) <= CHUNK_SIZE for c in chunks)

    # check overlap: the second chunk should start CHUNK_SIZE - CHUNK_OVERLAP into the original
    expected_overlap = content[CHUNK_SIZE - CHUNK_OVERLAP : CHUNK_SIZE]
    actual_overlap = chunks[1].page_content[:CHUNK_OVERLAP]
    assert actual_overlap == expected_overlap
