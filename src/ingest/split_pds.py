import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document


###############################################################################
#  Parameterisation
#  ---------------
#  Provide default values, but allow overrides through environment variables
#  so Optuna (or any script) can tweak them centrally via `.env`.
###############################################################################

DEFAULT_CHUNK_SIZE      = int(os.getenv("CHUNK_SIZE", "800"))
DEFAULT_CHUNK_OVERLAP   = int(os.getenv("CHUNK_OVERLAP", "80"))
LENGTH_FUNCTION         = len
IS_SEPARATOR_REGEX      = False


def split_documents(
    documents: list[Document],
    *,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None) -> list[Document]:

    _size    = chunk_size    or DEFAULT_CHUNK_SIZE
    chunk_overlap = chunk_overlap or DEFAULT_CHUNK_OVERLAP

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=LENGTH_FUNCTION,
        is_separator_regex=IS_SEPARATOR_REGEX,
    )

    return splitter.split_documents(documents)
