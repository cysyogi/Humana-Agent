import os

from langchain_openai import OpenAIEmbeddings
from langfuse import Langfuse
from langfuse.decorators import observe

langfuse = Langfuse()
@observe(as_type="generation")
def get_embedding():
    """
    Returns an OpenAIEmbeddings instance.
    Requires your OPENAI_API_KEY to be set in the environment.
    """
    return OpenAIEmbeddings(
        model="text-embedding-ada-002",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )
