#!/bin/bash
set -e

if [ ! -d "data/faiss_index" ]; then
    echo "No FAISS index found. Building index..."
    python src/indexer.py
else
    echo "FAISS index found. Skipping build."
fi

echo "Starting API server..."
exec uvicorn src.api:app --host 0.0.0.0 --port 8000