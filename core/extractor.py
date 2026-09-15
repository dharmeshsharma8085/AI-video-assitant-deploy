import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


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


def build_chain(system_prompt: str):

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{text}"),
        ]
    )

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    return chain


def extract_action_items(
    transcript: str
) -> str:

    if not transcript.strip():
        return "No action items found."

    chain = build_chain(
        "You are an expert meeting analyst. "
        "From the meeting transcript, extract all action items.\n\n"
        "For each action item provide:\n"
        "- Task description\n"
        "- Owner (who is responsible)\n"
        "- Deadline (if mentioned, otherwise write "
        "'Not specified')\n\n"
        "Format the result as a numbered list.\n"
        "If none are found, say "
        "'No action items found.'"
    )

    return chain.invoke(
        {"text": transcript}
    )


def extract_key_decisions(
    transcript: str
) -> str:

    if not transcript.strip():
        return "No key decisions found."

    chain = build_chain(
        "You are an expert meeting analyst. "
        "From the meeting transcript, extract all key "
        "decisions that were actually made.\n\n"
        "Do not include suggestions or discussions that "
        "were not finalized.\n\n"
        "Format the result as a numbered list.\n"
        "If none are found, say "
        "'No key decisions found.'"
    )

    return chain.invoke(
        {"text": transcript}
    )


def extract_questions(
    transcript: str
) -> str:

    if not transcript.strip():
        return "No open questions found."

    chain = build_chain(
        "You are an expert meeting analyst. "
        "From the meeting transcript, extract all unresolved "
        "questions or topics requiring follow-up.\n\n"
        "Format the result as a numbered list.\n"
        "If none are found, say "
        "'No open questions found.'"
    )

    return chain.invoke(
        {"text": transcript}
    )