import os
from langchain_community.embeddings import OpenAIEmbeddings


def get_embedding():
    """
    Returns an OpenAIEmbeddings instance.
    Requires your OPENAI_API_KEY to be set in the environment.
    """
    return OpenAIEmbeddings(
        model="text-embedding-ada-002",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )
