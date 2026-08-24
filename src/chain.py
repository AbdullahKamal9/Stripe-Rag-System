import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from retriever import get_basic_retriever, get_retriever

load_dotenv()

# LangSmith is auto-enabled from .env variabless
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=your_key
# LANGCHAIN_PROJECT=stripe-rag

PROMPT_TEMPLATE = """
You are a helpful Stripe documentation assistant.
Answer the question based ONLY on the context provided below.
If the answer is not in the context, say "I could not find this in the Stripe documentation."
Always mention which part of the documentation your answer comes from.

Context:
{context}

Question: {question}

Answer:
"""

def format_docs(docs):
    formatted = []
    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        content = doc.page_content
        formatted.append(f"[Source: {source}]\n{content}")
    return "\n\n---\n\n".join(formatted)

def get_chain(use_multi_query=False):
    if use_multi_query:
        retriever = get_retriever()
    else:
        retriever = get_basic_retriever()

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

# Cache at module level
_chain = None

def query(question: str, use_multi_query=False):
    global _chain
    if _chain is None:
        _chain = get_chain(use_multi_query=use_multi_query)
    response = _chain.invoke(question)
    return response

if __name__ == "__main__":
    print("Testing RAG chain...\n")

    # Test with basic retriever first (saves budget)
    test_questions = [
        "How do webhooks work in Stripe?",
        "What is the difference between PaymentIntent and Checkout?",
        "How do I handle payment failures?"
    ]

    for question in test_questions:
        print(f"Q: {question}")
        print(f"A: {query(question)}")
        print("\n" + "="*50 + "\n")