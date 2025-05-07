# src/services/openai_service.py

import os
from langchain_openai.chat_models import ChatOpenAI
from langfuse import Langfuse
from langfuse.decorators import observe
from dotenv import load_dotenv

load_dotenv()
langfuse = Langfuse()

LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4.1")

# singleton model with its own callback
_openai_model = ChatOpenAI(
    model_name=LLM_MODEL,
    temperature=0.0,
)

@observe()
def ask_openai(prompt: str) -> str:
    raw = _openai_model.invoke(prompt)
    return getattr(raw, "content", str(raw)).strip()
