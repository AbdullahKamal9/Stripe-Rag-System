"""Phase 3: run the full evaluation and log everything to one MLflow run.

Logs: pipeline params, quality (RAGAS), safety, toxicity, latency and cost metrics,
the per-question table, the prompt, and the test set.

Usage (from repo root):
    .venv\\Scripts\\python.exe eval\\run_mlflow.py --run-name reranker-v1
    .venv\\Scripts\\python.exe eval\\run_mlflow.py --limit 3 --run-name smoke
    .venv\\Scripts\\python.exe -m mlflow ui --backend-store-uri sqlite:///eval/mlflow.db
"""
import argparse
import hashlib
import inspect
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_eval as base  # noqa: E402  (applies the ragas compatibility shim)
import rag_metrics as rq  # noqa: E402
import prompt_registry  # noqa: E402

import mlflow  # noqa: E402
import pandas as pd  # noqa: E402

import chain  # noqa: E402
import indexer  # noqa: E402
import retriever  # noqa: E402

TRACKING_URI = "sqlite:///" + os.path.join(base.ROOT, "eval", "mlflow.db").replace("\\", "/")
ARTIFACT_ROOT = os.path.join(base.ROOT, "eval", "mlartifacts")
EXPERIMENT = "stripe-rag-eval"


def git_info():
    def run(*args):
        try:
            return subprocess.check_output(["git", *args], cwd=base.ROOT, text=True).strip()
        except Exception:
            return "unknown"

    return run("rev-parse", "--short", "HEAD"), bool(run("status", "--porcelain", "--", "src"))


def pipeline_params(rr_overrides):
    rr = {
        k: v.default
        for k, v in inspect.signature(retriever.get_reranked_retriever).parameters.items()
    }
    rr.update(rr_overrides)
    return {
        "generator_model": base.MODEL,
        "judge_model": base.MODEL,
        "temperature": 0,
        "embedding_model": "text-embedding-3-small",
        "chunk_size": indexer.CHUNK_SIZE,
        "chunk_overlap": indexer.CHUNK_OVERLAP,
        "retrieval": "hybrid(bm25+faiss)+cross-encoder-rerank",
        "reranker_model": retriever.RERANKER_MODEL,
        "candidates_k": rr["candidates_k"],
        "top_n": rr["top_n"],
        "rerank_min_score": rr["min_score"],
        "rerank_rel_margin": rr["rel_margin"],
        "prompt_sha": hashlib.sha256(chain.PROMPT_TEMPLATE.encode()).hexdigest()[:10],
        "price_in_per_1m_usd": base.PRICE_IN,
        "price_out_per_1m_usd": base.PRICE_OUT,
    }


# Thresholds are set below the measured exp2 scores to leave room for judge noise.
GATES = {
    "faithfulness": (">=", 0.90),
    "context_recall": (">=", 0.80),
    "context_precision": (">=", 0.75),
    "answer_relevancy": (">=", 0.75),
    "safe_rate": (">=", 0.95),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-name", default=None)
    ap.add_argument("--limit", type=int, default=None, help="answerable questions (smoke test)")
    ap.add_argument("--candidates-k", type=int, default=None)
    ap.add_argument("--top-n", type=int, default=None)
    ap.add_argument("--min-score", type=float, default=None)
    ap.add_argument("--rel-margin", type=float, default=None)
    ap.add_argument("--gate", action="store_true", help="exit non-zero if a metric misses its threshold")
    args = ap.parse_args()
    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY is not set (check .env)")

    rr_overrides = {
        k: v
        for k, v in {
            "candidates_k": args.candidates_k,
            "top_n": args.top_n,
            "min_score": args.min_score,
            "rel_margin": args.rel_margin,
        }.items()
        if v is not None
    }

    mlflow.set_tracking_uri(TRACKING_URI)
    if mlflow.get_experiment_by_name(EXPERIMENT) is None:
        mlflow.create_experiment(EXPERIMENT, artifact_location=pathlib_uri(ARTIFACT_ROOT))
    mlflow.set_experiment(EXPERIMENT)

    sha, dirty = git_info()
    with open(base.TESTSET, "rb") as f:
        testset_sha = hashlib.sha256(f.read()).hexdigest()[:10]

    rows = base.load_testset(args.limit)
    # The run starts before the pipeline so each question's trace is linked to it.
    with mlflow.start_run(run_name=args.run_name):
        # Autolog only around the pipeline; RAGAS judge calls would add hundreds of noisy traces.
        mlflow.langchain.autolog()
        try:
            df = base.run_pipeline(rows, rr_overrides, trace=True)
        finally:
            mlflow.langchain.autolog(disable=True)
        df = base.score_toxicity(df)
        quality = rq.score(df)
        df = df.merge(quality[["id"] + rq.METRIC_COLS], on="id", how="left")
        df = base.score_safety(df)
        summary = base.summarize(df)
        # context_relevance is not part of summarize(); add it with the other quality metrics.
        q = df[df["id"].str.startswith("q")]
        summary["context_relevance"] = float(q["context_relevance"].mean())
        summary["context_relevance_missing"] = int(q["context_relevance"].isna().sum())

        mlflow.log_params(pipeline_params(rr_overrides))
        # Record which registered prompt version this run used.
        prompt_version = prompt_registry.current_prompt_version()
        mlflow.log_params({"prompt_name": prompt_registry.PROMPT_NAME, "prompt_version": prompt_version})
        mlflow.set_tag("prompt_uri", f"prompts:/{prompt_registry.PROMPT_NAME}/{prompt_version}")
        mlflow.set_tags(
            {
                "git_sha": sha,
                "git_dirty_src": str(dirty),
                "testset_sha": testset_sha,
                "n_questions": str(len(df)),
                "smoke_test": str(args.limit is not None),
            }
        )
        mlflow.log_metrics({k: v for k, v in summary.items() if k != "n_questions"})

        table = df.drop(columns=["retrieved_contexts"]).copy()
        table["retrieved_contexts"] = df["retrieved_contexts"].apply(lambda c: "\n---\n".join(c))
        mlflow.log_table(table, artifact_file="per_question.json")
        mlflow.log_text(chain.PROMPT_TEMPLATE, "prompt.txt")
        mlflow.log_artifact(base.TESTSET, artifact_path="testset")
        run_id = mlflow.active_run().info.run_id

    print("\n=== LOGGED TO MLFLOW ===")
    for k, v in summary.items():
        print(f"{k:28s} {v:.4f}" if isinstance(v, float) else f"{k:28s} {v}")
    print(f"\nExperiment: {EXPERIMENT}   Run ID: {run_id}")
    print("View:  .venv\\Scripts\\python.exe -m mlflow ui --backend-store-uri " + TRACKING_URI)

    if args.gate:
        failed = []
        for name, (op, limit) in GATES.items():
            val = summary.get(name)
            ok = val is not None and val == val and (val >= limit if op == ">=" else val <= limit)
            print(f"GATE {name:20s} {val!s:>22} {op} {limit}  {'PASS' if ok else 'FAIL'}")
            if not ok:
                failed.append(name)
        if failed:
            sys.exit(f"Quality gate failed: {', '.join(failed)}")
        print("Quality gate passed")


def pathlib_uri(path):
    import pathlib

    return pathlib.Path(path).resolve().as_uri()


if __name__ == "__main__":
    main()
