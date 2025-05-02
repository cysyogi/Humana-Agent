from langchain_community.document_loaders import PyPDFDirectoryLoader


def load_document(folder_path: str):
    document_loader = PyPDFDirectoryLoader(folder_path)
    return document_loader.load()
