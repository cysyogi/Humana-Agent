import os
from langchain_community.chat_models import ChatOpenAI

# Load model from env
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4.1")

# Create singleton (reuse across app)
_openai_model = ChatOpenAI(
    model_name=LLM_MODEL,
    temperature=0.0,
)

def ask_openai(prompt: str) -> str:
    """
    Send prompt to OpenAI and return response text.
    """
    raw_response = _openai_model.invoke(prompt)

    if hasattr(raw_response, "content"):
        return raw_response.content.strip()

    return raw_response.strip()
