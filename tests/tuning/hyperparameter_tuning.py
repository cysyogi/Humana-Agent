"""
Bayesian hyper‑parameter tuning for RAG QA on medical‑insurance PDFs.

Usage:
  python tune_rag_optuna.py --trials 25 \
       --storage sqlite:///optuna_rag.db --study rag_param_search
"""

import argparse
import os
import shutil
import time
from statistics import mean
from typing import List

import optuna
from dotenv import load_dotenv

# ========== your project imports ========== #
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.schema import Document

from src.ingest.embedding_creator import get_embedding
from src.ingest.split_pds import split_documents
from tests.data.test_cases import TEST_CASES_100
from tests.utils.AI_QA_tester import query_and_validate
from src.db.populate_database import calculate_chunk_ids
from langchain_chroma import Chroma

# ---------- globals / config ---------- #
load_dotenv()

CHROMA_PATH  = os.getenv("CHROMA_PATH", "chroma")
DATA_PATH    = os.getenv("DATA_PATH",   "data")

DEFAULT_DOC_LOADER = PyPDFDirectoryLoader(DATA_PATH)
EMBEDDING_FN       = get_embedding()     # create once to reuse

# Ranges for the three tunables  ----------------
CHUNK_MIN, CHUNK_MAX   = 200, 600   # tokens
OVERLAP_MIN, OVERLAP_MAX = 0, 100   # tokens
K_MIN, K_MAX             = 3, 10    # integer


# -------------------------------------------------
#  core helpers
# -------------------------------------------------
def _clear_database(db_path: str = CHROMA_PATH):
    if os.path.exists(db_path):
        shutil.rmtree(db_path, ignore_errors=True)


def _index_docs(chunk_size: int, chunk_overlap: int) -> Chroma:
    """
    (Re)create the Chroma index with the given chunking params.
    Returns the in‑memory db handle (no need to persist between trials).
    """
    # 1. chunk the documents
    docs: List[Document] = DEFAULT_DOC_LOADER.load()
    chunks = split_documents(
        docs,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = calculate_chunk_ids(chunks)

    # 2. build fresh Chroma
    db = Chroma(embedding_function=EMBEDDING_FN)  # no persist_directory -> purely in‑memory
    ids = [c.metadata["id"] for c in chunks]
    db.add_documents(chunks, ids=ids)
    return db


def _run_suite(db: Chroma, k: int) -> float:
    """
    Execute the 100 boolean QA tests against the supplied DB & k.
    Returns success ratio (0.0‑1.0).
    """
    results = []
    for case in TEST_CASES_100:
        ok = query_and_validate(
            question=case["question"],
            expected_response=case["expected_response"],
            k=k,                      # <-- query_rag must forward this
            db=db                     # <-- query_rag must accept an existing db
        )
        expected_match = bool(case["should_match"])
        results.append(ok == expected_match)
    return mean(results)  # proportion correct


# -------------------------------------------------
#  Optuna objective
# -------------------------------------------------
def objective(trial: optuna.Trial) -> float:
    """
    One Optuna trial = one full build + evaluation.
    """
    chunk_size     = trial.suggest_int("chunk_size",   CHUNK_MIN, CHUNK_MAX,   step=50)
    chunk_overlap  = trial.suggest_int("chunk_overlap", OVERLAP_MIN, OVERLAP_MAX, step=25)
    k              = trial.suggest_int("k",             K_MIN, K_MAX)

    start = time.perf_counter()

    # (re)build vector store
    _clear_database()           # ensure a clean slate
    db = _index_docs(chunk_size, chunk_overlap)

    # evaluate
    success_ratio = _run_suite(db, k)

    duration = time.perf_counter() - start
    trial.set_user_attr("runtime_sec", round(duration, 2))

    # Optuna maximizes by default when direction="maximize"
    return success_ratio


# -------------------------------------------------
#  CLI wrapper
# -------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Tune RAG parameters with Optuna.")
    parser.add_argument("--trials", type=int, default=25, help="Number of Optuna trials.")
    parser.add_argument("--storage", type=str, default=None,
                        help="Optuna storage URI (e.g. sqlite:///rag.db).")
    parser.add_argument("--study", type=str, default="rag_optuna",
                        help="Study name (used if storage supplied).")
    args = parser.parse_args()

    study = optuna.create_study(
        direction="maximize",
        study_name=args.study,
        storage=args.storage,
        load_if_exists=True,
        sampler=optuna.samplers.TPESampler(multivariate=True, seed=42),
    )

    study.optimize(objective, n_trials=args.trials, show_progress_bar=True)

    print("\n===== BEST TRIAL =====")
    best = study.best_trial
    print(f"Accuracy  : {best.value:.4f}")
    print("Params    :", best.params)
    print("Run time  :", best.user_attrs.get("runtime_sec"), "sec")

    # ---- (optional) write best params back into .env ---- #
    out_env = ".env.best"
    with open(out_env, "w") as fp:
        for k, v in best.params.items():
            fp.write(f"{k.upper()}={v}\n")
    print(f"\nBest params saved to {out_env} – copy into your .env when ready.")


if __name__ == "__main__":
    main()
