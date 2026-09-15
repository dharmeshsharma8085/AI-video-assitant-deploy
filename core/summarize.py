# core/summarizer.py

import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()


def get_llm():

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set in .env"
        )

    return ChatOpenAI(
        model="gpt-5.6-luna",
        api_key=api_key,
        temperature=0.5
    )


def split_transcript(transcript: str) -> list:

    if not transcript.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=300
    )

    return splitter.split_text(
        transcript
    )


def summarize(transcript: str) -> str:

    if not transcript.strip():
        return "No transcript available to summarize."

    llm = get_llm()

    map_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Summarize this portion of a meeting or class "
                "transcript concisely. Keep the important information."
            ),
            (
                "human",
                "{text}"
            )
        ]
    )

    map_chain = (
        map_prompt
        | llm
        | StrOutputParser()
    )

    chunks = split_transcript(
        transcript
    )

    chunk_summaries = []

    for chunk in chunks:

        summary = map_chain.invoke(
            {"text": chunk}
        )

        chunk_summaries.append(
            summary
        )

    combined = "\n\n".join(
        chunk_summaries
    )

    combined_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert meeting summarizer. "
                "Combine these partial summaries into one final "
                "professional meeting summary using clear bullet points."
            ),
            (
                "human",
                "{text}"
            )
        ]
    )

    combined_chain = (
        combined_prompt
        | llm
        | StrOutputParser()
    )

    return combined_chain.invoke(
        {"text": combined}
    )


def generate_title(
    transcript: str
) -> str:

    if not transcript.strip():
        return "Untitled Meeting"

    llm = get_llm()

    title_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Based on the meeting transcript, generate a short "
                "professional meeting title (max 8 words). "
                "Only return the title, nothing else."
            ),
            (
                "human",
                "{text}"
            )
        ]
    )

    title_chain = (
        title_prompt
        | llm
        | StrOutputParser()
    )

    return title_chain.invoke(
        {
            "text": transcript[:2000]
        }
    ).strip()