# Humana-Agent
## Humana Policy & Provider AI Assistant

## 1 . Project Goal

A local demo chatbot that **answers insurance-policy questions and locates in-network hospitals** for Humana members. It shows how Retrieval-Augmented Generation (RAG), multi-agent orchestration, and external healthcare APIs can combine to deliver practical, trustworthy answers in a single conversational interface.

*Key objectives*

- Parse policy PDFs, index them semantically, and answer coverage questions with sourced citations.
- Query Humana’s FHIR Provider-Directory API (or any CMS-compliant directory) to list hospitals **in the user’s network**, then sort by distance with map data.
- Allow easy tuning of chunk size, embedding model, and prompts; fall back to a local LLM when offline.
- Keep the codebase modular so each agent can evolve (or be swapped) independently.

---

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

1. **ChatUI** (CLI or Gradio) collects the user’s greeting, then asks for **policyID/name** and an optional **ZIPcode** for location.
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

## 5. QuickStart (local demo)

. QuickStart (local demo)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=...
# Optional: export MAPS_API_KEY, FHIR_BASE_URL
python app/ui/gradio_app.py  # then open http://localhost:7860
```

---

## 6. Roadmap & Stretch Ideas

- **RAGbenchmark harness** with Recall\@K tracking.
- **Policy summarizer agent** (high‑level overview on demand).
- **Chunk visualizer** to inspect what text lives in each vector.
- **Hybrid lexical+semantic retrieval** for exact‑term questions.
- **Langfuse tracing** for debugging and latency metrics.

Feel free to fork and extend—each agent is only \~200lines and shares a common interface, so plugging in a new tool is straightforward.  Enjoy building!