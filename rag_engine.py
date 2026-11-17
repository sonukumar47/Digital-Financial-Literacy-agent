"""
IBM Granite-powered RAG engine for Digital Financial Literacy Agent.
Uses ChatWatsonx (chat API) with LCEL for granite-4-h-small and other chat models.
"""

import os
from typing import Optional
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_ibm import ChatWatsonx

load_dotenv()

# ---------------------------------------------------------------------------
# Helper: read from st.secrets (Streamlit Cloud) with fallback to os.getenv
# ---------------------------------------------------------------------------

def _get_secret(key: str, default: str = "") -> str:
    """Read a secret from st.secrets (Streamlit Cloud) or os.environ (local)."""
    try:
        import streamlit as st
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

IBM_CLOUD_API_KEY      = _get_secret("IBM_CLOUD_API_KEY")
IBM_WATSONX_PROJECT_ID = _get_secret("IBM_WATSONX_PROJECT_ID")
IBM_WATSONX_URL        = _get_secret("IBM_WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
GRANITE_MODEL_ID       = _get_secret("GRANITE_MODEL_ID", "ibm/granite-4-h-small")

EMBED_MODEL       = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_STORE_PATH = "faiss_index"

FINANCIAL_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        (
            "You are a knowledgeable Digital Financial Literacy Assistant for Indian users. "
            "Use ONLY the context provided to answer the user's question accurately. "
            "Use simple, clear language. If the question involves fraud or financial risk, "
            "clearly warn the user. If the context does not contain enough information, "
            "say so honestly rather than guessing."
        ),
    ),
    (
        "human",
        "Context from trusted financial sources:\n{context}\n\nQuestion: {question}",
    ),
])


# ---------------------------------------------------------------------------
# LLM Initialisation
# ---------------------------------------------------------------------------

def get_watsonx_llm() -> ChatWatsonx:
    """Initialise IBM Granite via watsonx.ai chat API."""
    return ChatWatsonx(
        model_id=GRANITE_MODEL_ID,
        url=IBM_WATSONX_URL,
        apikey=IBM_CLOUD_API_KEY,
        project_id=IBM_WATSONX_PROJECT_ID,
        params={
            "max_tokens": 512,
            "temperature": 0.3,
        },
    )


# ---------------------------------------------------------------------------
# Embeddings & Vector Store
# ---------------------------------------------------------------------------

def get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_vector_store(documents: list) -> FAISS:
    """Chunk documents and build a FAISS vector store."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " "],
    )
    chunks = splitter.split_documents(documents)
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(VECTOR_STORE_PATH)
    return vector_store


def load_vector_store() -> Optional[FAISS]:
    """Load an existing FAISS index from disk if available."""
    if os.path.exists(VECTOR_STORE_PATH):
        embeddings = get_embeddings()
        return FAISS.load_local(
            VECTOR_STORE_PATH,
            embeddings,
            allow_dangerous_deserialization=True,
        )
    return None


# ---------------------------------------------------------------------------
# RAG Chain (LCEL)
# ---------------------------------------------------------------------------

def _format_docs(docs) -> str:
    """Concatenate retrieved document chunks into a single context string."""
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(vector_store: FAISS) -> dict:
    """
    Build a LCEL RAG chain using IBM Granite (chat API).
    Returns a dict with keys 'chain' and 'retriever' for source lookup.
    """
    llm = get_watsonx_llm()
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )

    # LCEL chain: retrieve → format → chat prompt → LLM → parse
    rag_chain = (
        {
            "context":  retriever | _format_docs,
            "question": RunnablePassthrough(),
        }
        | FINANCIAL_PROMPT
        | llm
        | StrOutputParser()
    )

    return {"chain": rag_chain, "retriever": retriever}


def ask_question(chain_bundle: dict, question: str) -> dict:
    """
    Run a question through the RAG chain.
    Returns {"answer": str, "sources": list[str]}.
    """
    chain     = chain_bundle["chain"]
    retriever = chain_bundle["retriever"]

    answer = chain.invoke(question).strip()

    # Fetch source metadata separately
    source_docs = retriever.invoke(question)
    sources = []
    for doc in source_docs:
        src = doc.metadata.get("source", "")
        if src and src not in sources:
            sources.append(src)

    return {"answer": answer, "sources": sources}
