import os
from dotenv import load_dotenv
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI
from indexer import load_index, load_documents, chunk_documents

load_dotenv()

def get_retriever():
    print("Loading FAISS index...")
    vectorstore = load_index()

    print("Loading documents for BM25...")
    docs = load_documents()
    chunks = chunk_documents(docs)

    # Retriever 1: FAISS semantic search
    faiss_retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )

    # Retriever 2: BM25 keyword search
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = 4

    # Retriever 3: Hybrid = BM25 + FAISS combined
    hybrid_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, faiss_retriever],
        weights=[0.5, 0.5]
    )

    # Retriever 4: MultiQuery on top of hybrid
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    multi_query_retriever = MultiQueryRetriever.from_llm(
        retriever=hybrid_retriever,
        llm=llm
    )

    print("Retriever ready.")
    return multi_query_retriever


def get_basic_retriever():
    """
    Use this when you want fast retrieval without MultiQuery LLM calls.
    Good for testing without burning OpenAI budget.
    """
    vectorstore = load_index()
    docs = load_documents()
    chunks = chunk_documents(docs)

    faiss_retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )

    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = 4

    hybrid_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, faiss_retriever],
        weights=[0.5, 0.5]
    )

    return hybrid_retriever


RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
_reranker = None


def _get_reranker():
    global _reranker
    if _reranker is None:
        from sentence_transformers import CrossEncoder
        _reranker = CrossEncoder(RERANKER_MODEL)
    return _reranker


def get_reranked_retriever(candidates_k=10, top_n=6, min_score=-6.0, rel_margin=9.0):
    """
    Hybrid retrieval over a wide candidate pool, then a cross-encoder reranks
    the candidates against the question. The LLM only receives chunks that are
    in the top_n, score above min_score, and are within rel_margin of the best
    chunk. If nothing qualifies, the context is empty and the prompt makes the
    model say it does not have the information.
    """
    from langchain_core.runnables import RunnableLambda

    vectorstore = load_index()
    chunks = chunk_documents(load_documents())

    faiss_retriever = vectorstore.as_retriever(search_kwargs={"k": candidates_k})
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = candidates_k
    hybrid = EnsembleRetriever(
        retrievers=[bm25_retriever, faiss_retriever],
        weights=[0.5, 0.5]
    )
    reranker = _get_reranker()

    def retrieve(question):
        candidates = hybrid.invoke(question)
        if not candidates:
            return []
        scores = reranker.predict([(question, d.page_content) for d in candidates])
        ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
        cutoff = max(min_score, ranked[0][1] - rel_margin)
        ranked = [(d, s) for d, s in ranked if s >= cutoff]
        return [d for d, _ in ranked[:top_n]]

    return RunnableLambda(retrieve)


if __name__ == "__main__":
    # Test retrieval
    retriever = get_basic_retriever()

    test_query = "How do webhooks work in Stripe?"
    print(f"\nTesting query: {test_query}\n")

    results = retriever.invoke(test_query)

    for i, doc in enumerate(results):
        print(f"--- Chunk {i+1} ---")
        print(f"Source: {doc.metadata.get('source', 'unknown')}")
        print(f"Content: {doc.page_content[:200]}")
        print()