# core/transcriber.py

import os
import shutil
import requests
import whisper

from dotenv import load_dotenv
from pydub import AudioSegment


load_dotenv()


# ============================================================
# FFMPEG CONFIGURATION
# ============================================================

# ============================================================
# FFMPEG CONFIGURATION
# ============================================================

FFMPEG_EXE = shutil.which("ffmpeg")
FFPROBE_EXE = shutil.which("ffprobe")

if not FFMPEG_EXE:
    raise FileNotFoundError(
        "FFmpeg not found. Make sure FFmpeg is installed "
        "and available in PATH."
    )

if not FFPROBE_EXE:
    raise FileNotFoundError(
        "FFprobe not found. Make sure FFmpeg is installed "
        "and available in PATH."
    )

print(f"FFmpeg detected at: {FFMPEG_EXE}")
print(f"FFprobe detected at: {FFPROBE_EXE}")

# Tell pydub explicitly
AudioSegment.converter = FFMPEG_EXE
AudioSegment.ffprobe = FFPROBE_EXE


# ============================================================
# CONFIGURATION
# ============================================================

# Sarvam REST API accepts short audio.
# 25 seconds gives a safety margin.
SARVAM_PIECE_SECONDS = 25


WHISPER_MODEL = os.getenv(
    "WHISPER_MODEL",
    "small"
)


SARVAM_API_KEY = os.getenv(
    "SARVAM_API_KEY"
)


SARVAM_STT_URL = (
    "https://api.sarvam.ai/speech-to-text"
)


SARVAM_MODEL = os.getenv(
    "SARVAM_STT_MODEL",
    "saaras:v3"
)


# ============================================================
# WHISPER MODEL
# ============================================================

_model = None


def load_model():

    global _model

    if _model is None:

        print(
            f"Loading Whisper model: "
            f"{WHISPER_MODEL}..."
        )

        _model = whisper.load_model(
            WHISPER_MODEL
        )

        print(
            "Whisper model loaded successfully."
        )

    return _model


# ============================================================
# WHISPER TRANSCRIPTION
# ============================================================

def transcribe_chunk_whisper(
    chunk_path: str
) -> str:
    """
    Transcribe one audio chunk
    using local Whisper.
    """

    model = load_model()

    result = model.transcribe(
        chunk_path,
        task="transcribe",
        fp16=False
    )

    return result["text"].strip()


# ============================================================
# SARVAM API
# ============================================================

def _send_to_sarvam(
    piece_path: str
) -> str:
    """
    Send one short WAV file to Sarvam.
    """

    if not SARVAM_API_KEY:

        raise RuntimeError(
            "SARVAM_API_KEY is not set "
            "in .env"
        )


    headers = {
        "api-subscription-key":
        SARVAM_API_KEY
    }


    with open(
        piece_path,
        "rb"
    ) as audio_file:

        files = {
            "file": (
                os.path.basename(
                    piece_path
                ),
                audio_file,
                "audio/wav"
            )
        }


        data = {
            "model": SARVAM_MODEL,
            "mode": "translate"
        }


        response = requests.post(
            SARVAM_STT_URL,
            headers=headers,
            files=files,
            data=data,
            timeout=120
        )


    if not response.ok:

        print(
            f"\n❌ Sarvam Error: "
            f"{response.status_code}"
        )

        print(
            response.text
        )

        response.raise_for_status()


    result = response.json()


    if "transcript" not in result:

        raise RuntimeError(
            "Unexpected Sarvam response: "
            f"{result}"
        )


    return result[
        "transcript"
    ].strip()


# ============================================================
# SARVAM TRANSCRIPTION
# ============================================================

def transcribe_chunk_sarvam(
    chunk_path: str
) -> str:
    """
    Split a larger WAV chunk into
    25-second pieces and send them
    individually to Sarvam.
    """

    audio = AudioSegment.from_wav(
        chunk_path
    )


    piece_ms = (
        SARVAM_PIECE_SECONDS * 1000
    )


    transcripts = []


    total_pieces = (
        len(audio) + piece_ms - 1
    ) // piece_ms


    for i, start in enumerate(
        range(
            0,
            len(audio),
            piece_ms
        )
    ):

        piece = audio[
            start:start + piece_ms
        ]


        piece_path = (
            f"{chunk_path}_sv_{i}.wav"
        )


        piece.export(
            piece_path,
            format="wav"
        )


        try:

            print(
                f"  → Sarvam piece "
                f"{i + 1}/{total_pieces}"
            )


            text = _send_to_sarvam(
                piece_path
            )


            if text:

                transcripts.append(
                    text
                )


        finally:

            if os.path.exists(
                piece_path
            ):

                os.remove(
                    piece_path
                )


    return " ".join(
        transcripts
    ).strip()


# ============================================================
# ROUTER
# ============================================================

def transcribe_chunk(
    chunk_path: str,
    language: str = "english"
) -> str:
    """
    Select transcription engine.

    english  -> Whisper
    hinglish -> Sarvam
    """

    language = (
        language.lower().strip()
    )


    if language == "hinglish":

        return transcribe_chunk_sarvam(
            chunk_path
        )


    return transcribe_chunk_whisper(
        chunk_path
    )


# ============================================================
# TRANSCRIBE ALL
# ============================================================

def transcribe_all(
    chunks: list,
    language: str = "english"
) -> str:
    """
    Transcribe all audio chunks and
    combine them into one transcript.
    """

    if not chunks:

        raise ValueError(
            "No audio chunks provided."
        )


    language = (
        language.lower().strip()
    )


    engine = (
        "Sarvam AI"
        if language == "hinglish"
        else "Whisper"
    )


    print(
        f"Using {engine} "
        f"for transcription."
    )


    transcripts = []


    for i, chunk in enumerate(
        chunks
    ):

        print(
            f"Transcribing chunk "
            f"{i + 1}/{len(chunks)}..."
        )


        text = transcribe_chunk(
            chunk,
            language=language
        )


        if text:

            transcripts.append(
                text
            )


    print(
        "Transcription complete."
    )


    return " ".join(
        transcripts
    ).strip()