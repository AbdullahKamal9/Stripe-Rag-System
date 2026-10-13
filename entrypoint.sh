#!/bin/bash
set -e






if [ ! -f "data/faiss_index/index.faiss" ] || ! python src/indexer.py --check; then
    echo "FAISS index missing or outdated. Building index..."
    python src/indexer.py
else
    echo "FAISS index is current. Skipping build."
fi

echo "Starting API server..."
exec uvicorn src.api:app --host 0.0.0.0 --port 8000