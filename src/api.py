import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn
from chain import get_chain

load_dotenv()

app = FastAPI(
    title="Stripe Documentation RAG API",
    description="AI-powered Stripe documentation assistant with hybrid search",
    version="1.0.0"
)

# Request/Response models
class QueryRequest(BaseModel):
    question: str
    use_multi_query: bool = False

class QueryResponse(BaseModel):
    question: str
    answer: str
    status: str

class StatsResponse(BaseModel):
    total_chunks: int
    index_location: str
    model: str
    embedding_model: str
    status: str

# Cache chain at startup
_chain = None

def get_cached_chain(use_multi_query=False):
    global _chain
    if _chain is None:
        _chain = get_chain(use_multi_query=use_multi_query)
    return _chain

# Endpoints
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Stripe RAG API",
        "version": "1.0.0"
    }

@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Stripe RAG Assistant</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 24px; background: #f4f7fb; color: #111; }
                .container { max-width: 760px; margin: 0 auto; background: #fff; padding: 24px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); }
                h1 { margin-top: 0; }
                textarea { width: 100%; min-height: 120px; padding: 12px; border-radius: 8px; border: 1px solid #ccc; font-size: 16px; }
                button { margin-top: 16px; padding: 12px 20px; border: none; border-radius: 8px; background: #0065ff; color: #fff; font-size: 16px; cursor: pointer; }
                button:disabled { opacity: 0.6; cursor: not-allowed; }
                .response-box { white-space: pre-wrap; background: #f6f8ff; border: 1px solid #dde2ff; padding: 16px; border-radius: 10px; margin-top: 20px; min-height: 120px; }
                .history-item { margin-bottom: 18px; padding-bottom: 14px; border-bottom: 1px solid #e1e7ff; }
                .history-question { font-weight: 700; margin-bottom: 8px; }
                .history-answer { white-space: pre-wrap; color: #1b263b; }
                .history-empty { color: #6a7591; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Stripe RAG Assistant</h1>
                <p>Ask your Stripe knowledge base a question and get a response from the local RAG system.</p>
                <textarea id="question" placeholder="Type your question here..."></textarea>
                <br />
                <button id="askButton" onclick="askQuestion()">Ask</button>
                <button id="clearButton" onclick="clearHistory()" style="margin-left: 12px; background: #ff5f5f;">Clear history</button>
                <div id="response" class="response-box" style="margin-top: 20px;">Your answer/status will appear here.</div>
                <div id="history" class="response-box" style="margin-top: 16px;">
                    <div class="history-empty">No questions yet.</div>
                </div>
            </div>
            <script>
                function addHistoryItem(question, answer) {
                    const history = document.getElementById('history');
                    const empty = history.querySelector('.history-empty');
                    if (empty) {
                        empty.remove();
                    }
                    const item = document.createElement('div');
                    item.className = 'history-item';
                    item.innerHTML = `
                        <div class="history-question">Q: ${escapeHtml(question)}</div>
                        <div class="history-answer">A: ${escapeHtml(answer)}</div>
                    `;
                    history.prepend(item);
                }

                function escapeHtml(text) {
                    const map = {
                        '&': '&amp;',
                        '<': '&lt;',
                        '>': '&gt;',
                        '"': '&quot;',
                        "'": '&#039;'
                    };
                    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
                }

                function clearHistory() {
                    const history = document.getElementById('history');
                    history.innerHTML = '<div class="history-empty">No questions yet.</div>';
                }

                async function askQuestion() {
                    const button = document.getElementById('askButton');
                    const questionInput = document.getElementById('question');
                    const question = questionInput.value.trim();
                    const responseBox = document.getElementById('response');
                    if (!question) {
                        responseBox.textContent = 'Please enter a question first.';
                        return;
                    }
                    button.disabled = true;
                    responseBox.textContent = 'Loading...';
                    try {
                        const res = await fetch('/query', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ question })
                        });
                        const data = await res.json();
                        if (!res.ok) {
                            responseBox.textContent = data.detail || 'Error querying the RAG system.';
                        } else {
                            responseBox.textContent = `A: ${data.answer}`;
                            addHistoryItem(question, data.answer);
                            questionInput.value = '';
                        }
                    } catch (err) {
                        responseBox.textContent = err.message || 'Failed to reach the RAG server.';
                    } finally {
                        button.disabled = false;
                    }
                }
            </script>
        </body>
        </html>
        """
    )

@app.post("/query", response_model=QueryResponse)
def query_docs(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        chain = get_cached_chain(use_multi_query=request.use_multi_query)
        answer = chain.invoke(request.question)
        return QueryResponse(
            question=request.question,
            answer=answer,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/index")
def reindex_docs():
    """Reindex all documents. Use when docs are updated."""
    try:
        from indexer import load_documents, chunk_documents, create_index
        docs = load_documents()
        chunks = chunk_documents(docs)
        create_index(chunks)
        
        # Reset cached chain
        global _chain
        _chain = None
        
        return {
            "status": "success",
            "documents_loaded": len(docs),
            "chunks_created": len(chunks),
            "message": "Index rebuilt successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats", response_model=StatsResponse)
def get_stats():
    try:
        from indexer import load_documents, chunk_documents
        docs = load_documents()
        chunks = chunk_documents(docs)
        
        return StatsResponse(
            total_chunks=len(chunks),
            index_location="data/faiss_index",
            model="gpt-4o-mini",
            embedding_model="text-embedding-3-small",
            status="healthy"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
      uvicorn.run(app, host="0.0.0.0", port=8000)
