from dotenv import load_dotenv
from langchain_community.vectorstores import SKLearnVectorStore
from app.utils.ingest import load_and_split, get_embeddings

load_dotenv()

_vectorstore = None


def get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        print("Building vectorstore from documents...")
        chunks = load_and_split()
        embeddings = get_embeddings()
        _vectorstore = SKLearnVectorStore.from_documents(
            documents=chunks,
            embedding=embeddings,
        )
        print(f"Vectorstore ready with {len(chunks)} chunks")
    return _vectorstore


def reset_vectorstore():
    """Drop the in-memory index so the next query sees changed documents."""
    global _vectorstore
    _vectorstore = None


def retrieve_chunks(query: str, k: int = 3) -> str:
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(query, k=k)
    return "\n\n".join(f"[{d.metadata.get('source')}] {d.page_content}" for d in docs)