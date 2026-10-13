import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

# Paths
DOCS_PATH = "data/stripe_docs"
FAISS_INDEX_PATH = "data/faiss_index"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
# Bump when chunking/embedding changes so deployed indexes are rebuilt automatically.
INDEX_VERSION = f"chunk{CHUNK_SIZE}-{CHUNK_OVERLAP}-text-embedding-3-small"
VERSION_FILE = os.path.join(FAISS_INDEX_PATH, "index_version.txt")


def index_is_current():
    try:
        with open(VERSION_FILE) as f:
            return f.read().strip() == INDEX_VERSION
    except OSError:
        return False

def load_documents():
    print("Loading documents...")
    loader = DirectoryLoader(
        DOCS_PATH,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    docs = loader.load()
    print(f"Loaded {len(docs)} documents")
    return docs

def chunk_documents(docs):
    print("Chunking documents...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " "]
    )
    chunks = splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunks")
    return chunks

def create_index(chunks):
    print("Creating embeddings and FAISS index...")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(FAISS_INDEX_PATH)
    with open(VERSION_FILE, "w") as f:
        f.write(INDEX_VERSION)
    print(f"FAISS index saved to {FAISS_INDEX_PATH}")
    return vectorstore

def load_index():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    vectorstore = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore

if __name__ == "__main__":
    import sys

    if "--check" in sys.argv:
        sys.exit(0 if index_is_current() else 1)
    docs = load_documents()
    chunks = chunk_documents(docs)
    create_index(chunks)
    print("Indexing complete.")