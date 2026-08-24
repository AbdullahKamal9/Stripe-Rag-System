# Stripe RAG

Stripe RAG is a local documentation assistant that indexes Stripe Markdown files and combines FAISS vector search with BM25 keyword retrieval to surface precise, context-bound answers. It uses OpenAI for generation and FastAPI for a lightweight UI/API. Designed for private, reproducible local deployment and developer workflows.

## Features

- Hybrid retrieval: FAISS vector search + BM25 keyword matching
- Local Markdown docs indexing (data/stripe_docs)
- FastAPI UI + `/query` endpoint
- Uses OpenAI for answer generation (strict context-only responses by default)

## Requirements

- Python 3.10+
- A virtual environment (`venv` or `.venv`)
- OpenAI API key

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Environment

Create a `.env` file at the project root with your keys (do not commit this file):

```
OPENAI_API_KEY=sk-...
# optional: LANGCHAIN_API_KEY, LANGSMITH_API_KEY
```

## Indexing documents

If you update or add docs under `data/stripe_docs`, rebuild the FAISS index:

```powershell
# from project root (activate venv first)
python src/indexer.py
# or call the API endpoint
curl -X POST http://127.0.0.1:8000/index
```

## Run the API

Activate your venv, then run either:

```powershell
python src/api.py
# or (recommended) with uvicorn for autoreload
python -m uvicorn src.api:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 to use the UI.

## Example query

POST `/query` with JSON:

```json
{ "question": "How do I create a Checkout Session?" }
```

Response format:

```json
{ "question": "...", "answer": "...", "status": "success" }
```

## Security & Git

- `.env`, `venv/`, and `.venv/` are ignored by `.gitignore` — never commit secrets.
- Add remote repo and push code only (no API keys).

## Troubleshooting

- If imports fail, ensure you're using the correct virtual environment and `pip install -r requirements.txt`.
- If the chain returns "I could not find this...", try reindexing or increasing retriever `k` in `src/retriever.py`.

## Contributing

Small patches welcome. For large changes, open an issue first.

---

Created for local Stripe documentation retrieval and Q&A.
