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