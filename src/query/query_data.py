import argparse
import sys, os, json

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.services.openai_service import ask_openai


from src.ingest.embedding_creator import get_embedding

BASE_K = 5
CHROMA_PATH = "chroma"
POLICY_MAP_PATH = os.path.join("data", "policy_mapping.json")
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("question", help="Question to ask")
    parser.add_argument(
        "--policy",
        required=True,
        help="Policy ID (e.g. H1036269000SB25) or policy name"
    )
    parser.add_argument("-k", type=int, default=BASE_K, help="# chunks to retrieve")
    args = parser.parse_args()

    # ‑‑ resolve user‑supplied policy to collection name
    with open(POLICY_MAP_PATH) as f:
        policy_map: dict[str, str] = json.load(f)

    if args.policy in policy_map:
        policy_id = args.policy
    else:
        policy_id = next(
            (pid for pid, name in policy_map.items()
             if name.lower() == args.policy.lower()),
            None
        )
    if policy_id is None:
        raise ValueError(
            f"Unknown policy '{args.policy}'. "
            "Check data/policy_mapping.json."
        )

    query_rag(args.question, policy_id, k=args.k)


def query_rag(query_text: str, policy_id: str,k: int = 5) -> str:
    emb_fn = get_embedding()
    print(f"Querying {query_text}, using policy {policy_id}, k {k}")
    db    = Chroma(
        collection_name=policy_id,
        persist_directory=CHROMA_PATH,
        embedding_function=emb_fn
    )

    results     = db.similarity_search_with_score(query_text, k)
    docs, _     = zip(*results)
    context_txt = "\n\n---\n\n".join(d.page_content for d in docs)

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(
        context=context_txt, question=query_text
    )

    response_text = ask_openai(prompt)

    sources = [d.metadata.get("id") for d in docs]
    print("Response:", response_text)
    print("Sources:", sources)
    return response_text


if __name__ == "__main__":
    main()