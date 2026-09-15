from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions
)
from core.rag_engine import (
    build_rag_chain,
    ask_question
)
load_dotenv()


def run_pipeline(
    source: str,
    language: str = "english"
) -> dict:

    print("Starting AI Video Assistant...")

    if not source.strip():
        raise ValueError(
            "Source cannot be empty."
        )

    language = language.lower().strip()

    if language not in {
        "english",
        "hinglish"
    }:
        raise ValueError(
            "Language must be 'english' or 'hinglish'."
        )

    chunks = process_input(source)

    if not chunks:
        raise RuntimeError(
            "No audio chunks were created."
        )

    transcript = transcribe_all(
        chunks,
        language
    )

    if not transcript.strip():
        raise RuntimeError(
            "Transcription returned empty text."
        )

    print(
        "\nRaw transcription "
        f"(first 300 characters):\n"
        f"{transcript[:300]}"
    )

    print("\nGenerating title...")
    title = generate_title(transcript)

    print("Generating summary...")
    summary = summarize(transcript)

    print("Extracting action items...")
    action_items = extract_action_items(transcript)

    print("Extracting key decisions...")
    decisions = extract_key_decisions(transcript)

    print("Extracting open questions...")
    questions = extract_questions(transcript)

    print("Building RAG vector store...")
    rag_chain = build_rag_chain(transcript)

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }


if __name__ == "__main__":

    source = input(
        "Enter YouTube URL or local file path: "
    ).strip()

    language = (
        input(
            "Language (english/hinglish): "
        ).strip()
        or "english"
    )

    result = run_pipeline(
        source,
        language
    )

    print("\n" + "=" * 60)

    print(
        f"📌 Title: "
        f"{result['title']}"
    )

    print(
        f"\n📋 Summary:\n"
        f"{result['summary']}"
    )

    print(
        f"\n✅ Action Items:\n"
        f"{result['action_items']}"
    )

    print(
        f"\n🔑 Key Decisions:\n"
        f"{result['key_decisions']}"
    )

    print(
        f"\n❓ Open Questions:\n"
        f"{result['open_questions']}"
    )

    print("=" * 60)

    print(
        "\n💬 Chat with your meeting "
        "(type 'exit' to quit)\n"
    )

    rag_chain = result["rag_chain"]

    while True:

        question = input(
            "You: "
        ).strip()

        if question.lower() in {
            "exit",
            "quit",
            "q"
        }:
            print("👋 Goodbye!")
            break

        if not question:
            continue

        answer = ask_question(
            rag_chain,
            question
        )

        print(
            f"\n🤖 Assistant: "
            f"{answer}\n"
        )