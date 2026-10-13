"""RAG quality check: precision, recall, faithfulness, answer relevance, context relevance.

Usage (from repo root):
    .venv\\Scripts\\python.exe eval\\rag_metrics.py            # run pipeline + score
    .venv\\Scripts\\python.exe eval\\rag_metrics.py --reuse    # re-score saved eval\\results\\pipeline_output.csv
    .venv\\Scripts\\python.exe eval\\rag_metrics.py --limit 3  # quick smoke test
"""
import argparse
import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_eval as base  # noqa: E402  (applies the ragas compatibility shim)

import pandas as pd  # noqa: E402
from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # noqa: E402

METRIC_COLS = [
    "context_precision",
    "context_recall",
    "context_relevance",
    "faithfulness",
    "answer_relevancy",
]
TARGETS = {
    "context_precision": 0.80,
    "context_recall": 0.80,
    "context_relevance": 0.80,
    "faithfulness": 0.90,
    "answer_relevancy": 0.80,
}
EXPLAIN = {
    "context_precision": "retrieved chunks that are useful, with relevant ones ranked first",
    "context_recall": "needed information (from the reference) that was retrieved",
    "context_relevance": "retrieved context is relevant to the question",
    "faithfulness": "answer claims supported by the retrieved context (no hallucination)",
    "answer_relevancy": "answer actually addresses the question",
}


def load_rows(args):
    path = os.path.join(base.OUT_DIR, "pipeline_output.csv")
    if args.reuse:
        if not os.path.exists(path):
            sys.exit(f"{path} not found; run without --reuse first")
        df = pd.read_csv(path)
        df["retrieved_contexts"] = df["retrieved_contexts"].apply(ast.literal_eval)
        return df
    df = base.run_pipeline(base.load_testset(args.limit))
    os.makedirs(base.OUT_DIR, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
    return df


def score(df):
    from ragas import EvaluationDataset, evaluate
    from ragas.embeddings import LangchainEmbeddingsWrapper
    from ragas.llms import LangchainLLMWrapper
    from ragas.metrics import (
        ContextRelevance,
        Faithfulness,
        LLMContextPrecisionWithReference,
        LLMContextRecall,
        ResponseRelevancy,
    )
    from ragas.run_config import RunConfig

    judge = LangchainLLMWrapper(ChatOpenAI(model=base.MODEL, temperature=0))
    emb = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-small"))

    q = df[df["id"].str.startswith("q")].copy().reset_index(drop=True)

    def to_ds(frame):
        return EvaluationDataset.from_list(
            [
                {
                    "user_input": r.question,
                    "retrieved_contexts": list(r.retrieved_contexts),
                    "response": r.response,
                    "reference": r.reference,
                }
                for r in frame.itertuples()
            ]
        )

    rename = {
        "llm_context_precision_with_reference": "context_precision",
        "context_recall": "context_recall",
        "nv_context_relevance": "context_relevance",
        "faithfulness": "faithfulness",
        "answer_relevancy": "answer_relevancy",
    }

    def run(frame):
        res = evaluate(
            to_ds(frame),
            metrics=[
                LLMContextPrecisionWithReference(),
                LLMContextRecall(),
                ContextRelevance(),
                Faithfulness(),
                ResponseRelevancy(),
            ],
            llm=judge,
            embeddings=emb,
            run_config=RunConfig(timeout=300, max_workers=2, max_retries=5),
            show_progress=False,
        ).to_pandas().rename(columns=rename)
        missing = [c for c in METRIC_COLS if c not in res]
        if missing:
            sys.exit(f"RAGAS did not return: {missing}. Columns: {list(res.columns)}")
        return res

    out = q[["id", "category", "question"]].copy()
    for c in METRIC_COLS:
        out[c] = float("nan")

    # Judge calls can time out and leave NaN scores; retry only the affected rows.
    pending = list(out.index)
    for attempt in range(1, 4):
        res = run(q.loc[pending])
        for c in METRIC_COLS:
            out.loc[pending, c] = res[c].values
        pending = list(out.index[out[METRIC_COLS].isna().any(axis=1)])
        if not pending:
            break
        print(f"Attempt {attempt}: {len(pending)} rows still have missing scores, retrying...")
    return out


def report(out):
    pd.set_option("display.width", 220)
    pd.set_option("display.max_colwidth", 55)
    print("\n=== PER QUESTION ===")
    print(out[["id", "question"] + METRIC_COLS].round(2).to_string(index=False))

    print("\n=== OVERALL ===")
    for c in METRIC_COLS:
        v = out[c].mean()
        miss = int(out[c].isna().sum())
        status = "PASS" if v >= TARGETS[c] else "BELOW TARGET"
        print(f"{c:18s} {v:.3f}  target {TARGETS[c]:.2f}  {status:12s} missing={miss}  | {EXPLAIN[c]}")

    print("\n=== WEAKEST QUESTIONS (lowest average score) ===")
    out = out.assign(avg=out[METRIC_COLS].mean(axis=1))
    print(out.sort_values("avg").head(5)[["id", "question", "avg"]].round(2).to_string(index=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reuse", action="store_true", help="reuse saved per_question.csv")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY is not set (check .env)")

    df = load_rows(args)
    out = score(df)
    os.makedirs(base.OUT_DIR, exist_ok=True)
    path = os.path.join(base.OUT_DIR, "rag_quality.csv")
    out.to_csv(path, index=False, encoding="utf-8")
    report(out)
    print(f"\nSaved to {path}")


if __name__ == "__main__":
    main()
