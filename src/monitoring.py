"""Per-query production monitoring: latency, tokens, cost, retrieved sources, refusals.

Every /query call appends one JSON line to MONITORING_LOG. If MLFLOW_TRACKING_URI is set
and mlflow is installed, LangChain traces are also sent to MLflow.
"""
import json
import os
import threading
import time
from datetime import datetime, timezone

from langchain_core.callbacks import BaseCallbackHandler

# gpt-4o-mini, USD per 1M tokens (same prices as eval/run_eval.py)
PRICE_IN, PRICE_OUT = 0.15, 0.60
REFUSAL = "I could not find this in the Stripe documentation."
LOG_PATH = os.getenv("MONITORING_LOG", "data/monitoring/queries.jsonl")
_lock = threading.Lock()


class QueryStats(BaseCallbackHandler):
    """Collects token usage and retrieved sources for one chain invocation."""

    def __init__(self):
        self.tokens_in = 0
        self.tokens_out = 0
        self.sources = []

    def on_chain_end(self, outputs, **kwargs):
        # The reranker lambda finishes after the inner retrievers, so the last
        # list of documents seen is the final context sent to the LLM.
        if isinstance(outputs, list) and all(hasattr(d, "metadata") for d in outputs):
            self.sources = [d.metadata.get("source", "unknown") for d in outputs]

    def on_llm_end(self, response, **kwargs):
        for gens in response.generations:
            for g in gens:
                usage = getattr(getattr(g, "message", None), "usage_metadata", None) or {}
                self.tokens_in += usage.get("input_tokens", 0)
                self.tokens_out += usage.get("output_tokens", 0)


def run_monitored(chain, question):
    """Invoke the chain and return (answer, record). The record is also logged to disk."""
    stats = QueryStats()
    start = time.perf_counter()
    error = None
    answer = None
    try:
        answer = chain.invoke(question, config={"callbacks": [stats]})
        return answer, _log(question, answer, start, stats, None)
    except Exception as e:
        error = f"{type(e).__name__}: {e}"
        _log(question, answer, start, stats, error)
        raise


def _log(question, answer, start, stats, error):
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "question": question,
        "answer": answer,
        "latency_s": round(time.perf_counter() - start, 3),
        "tokens_in": stats.tokens_in,
        "tokens_out": stats.tokens_out,
        "cost_usd": (stats.tokens_in * PRICE_IN + stats.tokens_out * PRICE_OUT) / 1_000_000,
        "n_chunks": len(stats.sources),
        "sources": stats.sources,
        "refused": bool(answer) and REFUSAL in answer,
        "error": error,
    }
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with _lock, open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except OSError:
        pass  # monitoring must never break a request
    return record


def summarize(limit=1000):
    """Aggregate the most recent `limit` logged queries."""
    try:
        with open(LOG_PATH, encoding="utf-8") as f:
            rows = [json.loads(line) for line in f.readlines()[-limit:]]
    except OSError:
        rows = []
    if not rows:
        return {"queries": 0}
    lat = sorted(r["latency_s"] for r in rows)

    def pct(p):
        return lat[min(len(lat) - 1, int(p * len(lat)))]

    n = len(rows)
    return {
        "queries": n,
        "latency_p50_s": pct(0.5),
        "latency_p95_s": pct(0.95),
        "total_cost_usd": round(sum(r["cost_usd"] for r in rows), 6),
        "avg_cost_usd": sum(r["cost_usd"] for r in rows) / n,
        "refusal_rate": sum(r["refused"] for r in rows) / n,
        "error_rate": sum(1 for r in rows if r["error"]) / n,
        "avg_chunks": sum(r["n_chunks"] for r in rows) / n,
    }


def enable_mlflow_tracing():
    """Send LangChain traces to MLflow when MLFLOW_TRACKING_URI is configured."""
    uri = os.getenv("MLFLOW_TRACKING_URI")
    if not uri:
        return False
    try:
        import mlflow

        mlflow.set_tracking_uri(uri)
        mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT", "stripe-rag-production"))
        mlflow.langchain.autolog()
        return True
    except Exception:
        return False
