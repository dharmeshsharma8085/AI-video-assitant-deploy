# core/vector_store.py

import hashlib

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


CHROMA_DIR = "vector_db"

COLLECTION_NAME = "meeting_transcript"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={
            "device": "cpu"
        }
    )


def get_collection_name(
    transcript: str
) -> str:

    transcript_hash = hashlib.md5(
        transcript.encode("utf-8")
    ).hexdigest()[:12]

    return (
        f"{COLLECTION_NAME}_{transcript_hash}"
    )


def build_vector_store(
    transcript: str
) -> Chroma:

    if not transcript.strip():
        raise ValueError(
            "Transcript cannot be empty."
        )

    print("Building Vector Store...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(
        transcript
    )

    docs = [
        Document(
            page_content=chunk,
            metadata={
                "chunk_index": i
            }
        )
        for i, chunk in enumerate(chunks)
    ]

    embeddings = get_embeddings()

    collection_name = get_collection_name(
        transcript
    )

    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=CHROMA_DIR
    )

    print(
        "Vector Store built successfully."
    )

    return vector_store


def load_vector_store(
    transcript: str
) -> Chroma:

    if not transcript.strip():
        raise ValueError(
            "Transcript cannot be empty."
        )

    embeddings = get_embeddings()

    collection_name = get_collection_name(
        transcript
    )

    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR
    )

    return vector_store


def get_retriever(
    vector_store: Chroma,
    k: int = 4
):

    if k <= 0:
        raise ValueError(
            "k must be greater than 0."
        )

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k
        }
    )