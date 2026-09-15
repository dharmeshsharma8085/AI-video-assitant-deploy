# core/rag.py

import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda
)

from core.vector_store import (
    build_vector_store,
    load_vector_store,
    get_retriever
)


load_dotenv()


def get_llm():

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set in .env"
        )

    return ChatOpenAI(
        model="gpt-5.6-luna",
        api_key=api_key,
        temperature=0.5
    )


def format_docs(docs):

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


def _create_rag_chain(
    retriever,
    llm
):

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert meeting assistant.

Answer the user's question based ONLY on the
meeting transcript context provided below.

If the answer is not found in the context, say:

"I could not find this information in the meeting transcript."

Always be concise and precise.
If quoting someone, mention it clearly.

Context from meeting transcript:
{context}"""
            ),
            (
                "human",
                "{question}"
            )
        ]
    )

    rag_chain = (
        {
            "context": (
                retriever
                | RunnableLambda(format_docs)
            ),
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def build_rag_chain(
    transcript: str
):

    if not transcript.strip():
        raise ValueError(
            "Transcript cannot be empty."
        )

    vector_store = build_vector_store(
        transcript
    )

    retriever = get_retriever(
        vector_store,
        k=4
    )

    llm = get_llm()

    return _create_rag_chain(
        retriever,
        llm
    )


def load_rag_chain(
    transcript: str
):

    if not transcript.strip():
        raise ValueError(
            "Transcript cannot be empty."
        )

    vector_store = load_vector_store(
        transcript
    )

    retriever = get_retriever(
        vector_store,
        k=4
    )

    llm = get_llm()

    return _create_rag_chain(
        retriever,
        llm
    )


def ask_question(
    rag_chain,
    question: str
) -> str:

    if not question.strip():
        raise ValueError(
            "Question cannot be empty."
        )

    print(
        f"QUESTION: {question}"
    )

    answer = rag_chain.invoke(
        question
    )

    print(
        f"ANSWER: {answer}"
    )

    return answer