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


def query_rag(query_text: str):
    emb_fn = get_embedding()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=emb_fn)

    results = db.similarity_search_with_score(query_text, k=5)
    docs, _scores = zip(*results)
    context_text = "\n\n---\n\n".join(doc.page_content for doc in docs)

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = LLMChain(
        llm=ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.0,
        ),
        prompt=prompt,
    )

    response_text = chain.run(context=context_text, question=query_text)
    sources = [doc.metadata.get("id") for doc in docs]

    print("Response:", response_text)
    print("Sources:", sources)
    return response_text


if __name__ == "__main__":
    load_dotenv()
    main()
