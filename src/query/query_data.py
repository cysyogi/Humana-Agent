import argparse

from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from src.ingest.embedding_creator import get_embedding

CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_rag(args.query_text)


def query_rag(query_text: str) -> str:
    emb_fn = get_embedding()
    db    = Chroma(persist_directory=CHROMA_PATH, embedding_function=emb_fn)

    results     = db.similarity_search_with_score(query_text, k=5)
    docs, _     = zip(*results)
    context_txt = "\n\n---\n\n".join(d.page_content for d in docs)

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(
        context=context_txt, question=query_text
    )

    # 4) call the model directly via .invoke()
    model = ChatOpenAI(
        model_name="gpt-4.1",  # or "gpt-4" / "gpt-3.5-turbo"
        temperature=0.0,
    )
    raw_response = model.invoke(prompt)

    if hasattr(raw_response, "content"):
        response_text = raw_response.content
    else:
        response_text = raw_response

    sources = [d.metadata.get("id") for d in docs]
    print("Response:", response_text)
    print("Sources:", sources)
    return response_text


if __name__ == "__main__":
    load_dotenv()
    main()
