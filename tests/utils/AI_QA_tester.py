from dotenv import load_dotenv

from src.query.query_data import query_rag
from langchain_openai.chat_models import ChatOpenAI
from langfuse import Langfuse
from langfuse.decorators import observe

load_dotenv()
langfuse = Langfuse()

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""



@observe(name="testing")
def query_and_validate(question: str, source: str ,expected_response: str):
    actual_response = query_rag(question,source).strip()

    prompt = EVAL_PROMPT.format(
        expected_response=expected_response,
        actual_response=actual_response,
    )

    model = ChatOpenAI(
        model_name="gpt-4.1",
        temperature=0.0,
    )
    evaluation_results = model.predict(prompt).strip().lower()

    # 4) assert and color‐print
    if evaluation_results.startswith("true"):
        print("\033[92m" + "✅ matches expected" + "\033[0m")
        return True
    elif evaluation_results.startswith("false"):
        print("\033[91m" + "❌ does not match expected" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Unclear evaluation result: {evaluation_results!r}"
        )
