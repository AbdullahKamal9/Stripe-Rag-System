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

## Evaluation & MLOps

The pipeline is evaluated on a 28-question golden set ([eval/testset.jsonl](eval/testset.jsonl): 20 answerable, 8 adversarial/off-topic). RAGAS scores answer quality, and every run is tracked in MLflow. `gpt-4o-mini` is both the generator and the judge.

| Area | Metrics | Tool |
|---|---|---|
| Retrieval | Context precision, context recall, context relevance | RAGAS |
| Generation | Faithfulness, answer relevancy | RAGAS |
| Safety | Safe-response rate (injection, fraud, off-topic) | LLM judge (RAGAS `AspectCritic`) |
| Toxicity | Max / mean toxicity | Detoxify |
| Performance | Latency p50/p95, tokens, cost per query | Timers + token pricing |

### Results

| Metric | Baseline | Final (reranker + strict prompt) |
|---|---|---|
| Context precision | 63.6% | 82.2% |
| Context recall | 95.8% | 91.7% |
| Context relevance | 97.5% | 100% |
| Faithfulness | 79.0% | 96.9% |
| Answer relevancy | 84.8% | 83.5% |
| Safe rate | 89.3% (judge false positives) | 96.4% |

Changes that moved the numbers: 1000-character heading-aware chunks, a cross-encoder reranker (`cross-encoder/ms-marco-MiniLM-L-6-v2`) with a relative score cutoff, and a strict grounded prompt. Three runs were compared in MLflow (`rel_margin` 6 vs 9, `top_n` 4 vs 6); the winner (`rel_margin=9`, `top_n=6`) is now the default.

**Limitations:** 20 answerable questions and an LLM judge, so differences of about 3 points are noise. References for q10–q20 are from general knowledge and not verified against the docs. Cost covers only the app's LLM calls, not the judge. Latency was measured on a busy machine and is not reliable; the reranker runs on CPU and is the slowest step.

### MLflow usage

- **Experiment tracking:** `eval/run_mlflow.py` logs params (retriever settings, chunking, model), about 23 metrics, git/test-set tags, the prompt, and a per-question table to the `stripe-rag-eval` experiment.
- **Tracing:** each evaluation question is one trace (retrieval, rerank, prompt, LLM), linked to its run. The API also traces queries when `MLFLOW_TRACKING_URI` is set (`mlflow.langchain.autolog()`).
- **Prompt Registry:** `eval/prompt_registry.py` versions the prompt as `stripe-rag-answer` (v1 `baseline`, v2 `production`); each run records its `prompt_version`.
- **CI quality gate:** `--gate` fails the build if faithfulness < 0.90, recall < 0.80, precision < 0.75, answer relevancy < 0.75 or safe rate < 0.95. It runs in `.github/workflows/deploy.yml` before the image is built (needs the `OPENAI_API_KEY` secret).
- **Production monitoring:** every `/query` is logged to `data/monitoring/queries.jsonl` (latency, tokens, cost, sources, refusals); `GET /monitoring` summarises it.

```bash
pip install -r requirements.txt -r eval/requirements-eval.txt
python eval/run_mlflow.py --run-name my-run          # full evaluation + MLflow logging
python eval/run_mlflow.py --limit 3 --gate           # quick check with the CI gate
python eval/prompt_registry.py                       # register prompt versions
python -m mlflow server --backend-store-uri sqlite:///eval/mlflow.db --port 5000
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
