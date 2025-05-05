# Humana-Agent – Policy & Provider AI Assistant

**Humana-Agent** is an AI-powered chatbot that helps users query their insurance policy information and locate in‑network providers. It uses a Retrieval‑Augmented Generation (RAG) approach with specialized agents to deliver accurate, context‑rich answers.

## Overview

- **Purpose:**  
  Answer insurance policy questions (coverage, costs, etc.) and find in‑network providers for Humana members via a chat interface.

- **Architecture:**  
  The system is modular, with an **Orchestrator** routing queries to:
  - **PDF Q&A Agent:** Retrieves and answers coverage questions from indexed policy PDFs.  
  - **Hospital Search Agent:** Queries a FHIR Provider Directory API and ranks by distance.  
  - **LLM Client:** Generates the final answer using retrieved data.

- **Technology:**  
  - **Chroma** vector database for semantic search of policy text.  
  - **Chainlit** for the web‐based chat UI.  
  - **LangChain**, **OpenAI API** (or fallback local LLM), **Optuna** for tuning.
## 2 . Simplified Architecture

```text
┌────────┐   1. chat msg   ┌──────────────┐
│  User  │ ───────────────▶│   Chat UI    │
└────────┘                 └────┬─────────┘
                                │2. route
                                ▼
                         ┌──────────────┐
                         │ Orchestrator │
                         └──┬────┬──────┘
         ┌───────────────►  │    │                ▲ 7. answer
 3. Q&A  │                  ▼    ▼                │
         │        ┌───────────┐ 5. search   ┌─────────────┐
         │        │  PDF Q&A  │────────────▶│  FHIR API   │
         │        └────┬──────┘             └─────────────┘
         │4. fetch      │                           ▲
┌─────────────┐         ▼6. prompts                 │6b geo
│ Vector DB   │◀────────│   LLM Client │────────────┤
└─────────────┘         └──────────────┘            │
                                                    ▼
                                              ┌──────────────┐
                                              │ Maps / Geo   │
                                              └──────────────┘
```
*Only the essential paths are shown—additional agents (e.g. WebSearch) plug in the same way.*

---

## 3. Module Flow

1. **ChatUI** (CLI or chainlit) collects the user’s greeting, then asks for **policyID/name** and an optional **ZIPcode** for location.
2. **Orchestrator** tags each user message with an *intent* (simple keyword rules).  It forwards:
   - *Coverage / cost* queries ➜ **PDFQ&AAgent**.
   - *Provider / hospital* queries ➜ **HospitalSearchAgent**.
3. **PDFQ&AAgent**
   - Loads the matching policy PDF (lazy‑load on first request).
   - Splits text into chunks (configurable size& overlap) ➜ **VectorDB**.
   - For a question, performs semantic KNN **within that policy’s chunks**.
   - Passes top‑K snippets + question to **LLMClient** to craft an answer with in‑text citations.
4. **HospitalSearchAgent**
   - Reads the policy’s `InsurancePlan` from the **FHIRProvider DirectoryAPI** to discover its `network`.
   - Queries `/Location?network=<id>&type=hospital`.
   - Geo‑codes results (local Haversine or **MapsAPI**), sorts by distance from the user’s ZIP, and returns a list.
   - The **LLMClient** optionally rewrites or formats the final answer.
5. **LLMClient** tries the primary cloud model first; on error or offline mode it falls back to a local model.
6. The **Orchestrator** merges the agent’s payload and sends a final, chat‑friendly reply back to the **ChatUI**.

---

## 4. Setup and Installation

1. **Clone & Install**  
   ```bash
   git clone https://github.com/cysyogi/Humana-Agent.git
   cd Humana-Agent
   python -m venv .venv && source .venv/bin/activate   # optional
   pip install -r requirements.txt
   ```

2. **Configure `.env`**  
   In the project root, create a `.env` file:
   ```env
   OPENAI_API_KEY=<your_openai_key>
   FHIR_BASE_URL=<FHIR_provider_directory_url>   # optional
   MAPS_API_KEY=<geocoding_api_key>               # optional
   ```

3. **Initialize the Vector DB**  
   Place policy PDFs in `data/`, then run:
   ```bash
   python3 -m src.db.populate_database --reset
   ```
   This loads PDFs, chunks text, generates embeddings, and stores them in `./chroma/`.

4. **Run the Chainlit App**  
   ```bash
   export PYTHONPATH=.
   chainlit run src/chainlit/app.py
   ```
   A browser window will open with the chat UI. Ask questions like “What is my ER copay?” or “Find in‑network hospitals near 30309.”

## 5. Testing

```bash
pytest -n 2
```
> **Note:** Limit to 2 parallel jobs to avoid OpenAI API rate‑limit (HTTP 429) errors.

## 6. Hyperparameter Tuning with Optuna

```bash
python tests/tuning/hyperparameter_tuning.py --trials 25      --storage sqlite:///optuna_rag.db --study rag_param_search
```
Then update your `.env` with the best `CHUNK_SIZE`/`CHUNK_OVERLAP`.