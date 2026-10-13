"""Prompt versioning with the MLflow Prompt Registry.

The prompt in src/chain.py stays the source of truth. This module registers it (and the
original loose prompt) as versions of one named prompt, moves the `production` alias,
and lets evaluation runs record which prompt version they used.

Usage (from repo root):
    .venv\\Scripts\\python.exe eval\\prompt_registry.py            # register + set aliases
    .venv\\Scripts\\python.exe eval\\prompt_registry.py --list     # show versions and aliases
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "src"))

import mlflow
from mlflow import genai

PROMPT_NAME = "stripe-rag-answer"
ROOT = os.path.abspath(os.path.join(HERE, ".."))
TRACKING_URI = "sqlite:///" + os.path.join(ROOT, "eval", "mlflow.db").replace("\\", "/")

# The first prompt version, before the grounding rules were added.
V1_TEMPLATE = """
You are a helpful Stripe documentation assistant.
Answer the question based ONLY on the context provided below.
If the answer is not in the context, say "I could not find this in the Stripe documentation."
Always mention which part of the documentation your answer comes from.

Context:
{context}

Question: {question}

Answer:
"""


def to_mlflow(template):
    """LangChain uses {var}; the MLflow registry uses {{var}}."""
    return re.sub(r"(?<!\{)\{(\w+)\}(?!\})", r"{{\1}}", template)


def _versions():
    from mlflow import MlflowClient

    try:
        return list(MlflowClient().search_prompt_versions(PROMPT_NAME))
    except Exception:
        return []  # prompt not registered yet


def find_version(template):
    """Return the registered version whose text equals `template`, or None."""
    target = to_mlflow(template).strip()
    for pv in _versions():
        if pv.template.strip() == target:
            return pv.version
    return None


def register_if_new(template, message):
    v = find_version(template)
    if v is not None:
        return v
    return genai.register_prompt(PROMPT_NAME, to_mlflow(template), commit_message=message).version


def register_all():
    import chain

    v1 = register_if_new(V1_TEMPLATE, "Original loose prompt (baseline)")
    v2 = register_if_new(
        chain.PROMPT_TEMPLATE, "Strict grounded prompt: only-from-context, exact refusal, injection-safe"
    )
    genai.set_prompt_alias(PROMPT_NAME, "baseline", v1)
    genai.set_prompt_alias(PROMPT_NAME, "production", v2)
    return v1, v2


def current_prompt_version():
    """Version number of src/chain.py's prompt, registering it if it is new."""
    import chain

    return register_if_new(chain.PROMPT_TEMPLATE, "Registered automatically by an evaluation run")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_registry_uri(TRACKING_URI)
    if args.list:
        for pv in _versions():
            print(f"v{pv.version}  aliases={pv.aliases}  {pv.commit_message}")
        return
    v1, v2 = register_all()
    print(f"{PROMPT_NAME}: v{v1} = baseline, v{v2} = production")


if __name__ == "__main__":
    main()
