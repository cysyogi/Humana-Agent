from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document


# constants for chunking
CHUNK_SIZE = 800
CHUNK_OVERLAP = 80
LENGTH_FUNCTION = len
IS_SEPARATOR_REGEX = False


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=LENGTH_FUNCTION,
        is_separator_regex=IS_SEPARATOR_REGEX,
    )
    return text_splitter.split_documents(documents)
