# utils/audio_processor.py

import os
import shutil

import yt_dlp

from pydub import AudioSegment


# ============================================================
# CONFIGURATION
# ============================================================

FFMPEG_EXE = shutil.which("ffmpeg")
FFPROBE_EXE = shutil.which("ffprobe")


if not FFMPEG_EXE:
    raise FileNotFoundError(
        "FFmpeg not found in PATH."
    )


if not FFPROBE_EXE:
    raise FileNotFoundError(
        "FFprobe not found in PATH."
    )


# Tell Pydub where FFmpeg is located
AudioSegment.converter = FFMPEG_EXE
AudioSegment.ffprobe = FFPROBE_EXE


DOWNLOAD_DIR = "downloads"

os.makedirs(
    DOWNLOAD_DIR,
    exist_ok=True
)


# ============================================================
# YOUTUBE AUDIO DOWNLOAD
# ============================================================

def download_youtube_audio(
    url: str
) -> str:
    """
    Download YouTube audio and convert
    it to WAV using FFmpeg.
    """

    output_path = os.path.join(
        DOWNLOAD_DIR,
        "%(title)s.%(ext)s"
    )


    ydl_opts = {

        # Let yt-dlp choose an available audio format
        "format": "bestaudio/best",

        # Output filename
        "outtmpl": output_path,

        # FFmpeg path
        "ffmpeg_location": FFMPEG_EXE,

        # Convert downloaded audio to WAV
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],

        # Do not download playlist
        "noplaylist": True,

        # Keep terminal output clean
        "quiet": True,

        # No unnecessary warnings
        "no_warnings": True,
    }


    try:

        with yt_dlp.YoutubeDL(
            ydl_opts
        ) as ydl:

            info = ydl.extract_info(
                url,
                download=True
            )

            filename = ydl.prepare_filename(
                info
            )


    except Exception as e:

        raise RuntimeError(
            f"YouTube download failed: {e}"
        ) from e


    # FFmpeg converts the downloaded file to WAV
    wav_path = (
        os.path.splitext(filename)[0]
        + ".wav"
    )


    if not os.path.exists(
        wav_path
    ):

        raise FileNotFoundError(
            f"Failed to create WAV file: "
            f"{wav_path}"
        )


    return wav_path


# ============================================================
# LOCAL FILE → WAV
# ============================================================

def convert_to_wav(
    input_path: str
) -> str:
    """
    Convert any supported audio/video file
    to WAV using Pydub + FFmpeg.
    """

    if not os.path.exists(
        input_path
    ):

        raise FileNotFoundError(
            f"Input file not found: "
            f"{input_path}"
        )


    output_path = (
        os.path.splitext(input_path)[0]
        + "_converted.wav"
    )


    try:

        audio = AudioSegment.from_file(
            input_path
        )


        # Convert to:
        # Mono
        # 16 kHz
        audio = (
            audio
            .set_channels(1)
            .set_frame_rate(16000)
        )


        audio.export(
            output_path,
            format="wav"
        )


    except Exception as e:

        raise RuntimeError(
            f"Failed to convert file to WAV: {e}"
        ) from e


    return output_path


# ============================================================
# CHUNK AUDIO
# ============================================================

def chunk_audio(
    wav_path: str,
    chunk_minutes: int = 10
) -> list:
    """
    Split WAV audio into smaller chunks.

    Default chunk size:
    10 minutes
    """

    if not os.path.exists(
        wav_path
    ):

        raise FileNotFoundError(
            f"WAV file not found: "
            f"{wav_path}"
        )


    if chunk_minutes <= 0:

        raise ValueError(
            "chunk_minutes must be greater than 0"
        )


    audio = AudioSegment.from_wav(
        wav_path
    )


    chunk_ms = (
        chunk_minutes
        * 60
        * 1000
    )


    chunks = []


    for i, start in enumerate(
        range(
            0,
            len(audio),
            chunk_ms
        )
    ):

        chunk = audio[
            start:start + chunk_ms
        ]


        chunk_path = (
            f"{wav_path}"
            f"_chunk_{i}.wav"
        )


        chunk.export(
            chunk_path,
            format="wav"
        )


        chunks.append(
            chunk_path
        )


    return chunks


# ============================================================
# MAIN AUDIO PROCESSOR
# ============================================================

def process_input(
    source: str
) -> list:
    """
    Process either:

    1. YouTube URL
    2. Local audio/video file

    Returns:
        list of WAV chunk paths
    """

    if not source:

        raise ValueError(
            "Source cannot be empty."
        )


    # --------------------------------------------------------
    # YouTube URL
    # --------------------------------------------------------

    if (
        source.startswith("http://")
        or source.startswith("https://")
    ):

        print(
            "Detected YouTube URL."
        )


        print(
            "Downloading audio..."
        )


        wav_path = (
            download_youtube_audio(
                source
            )
        )


    # --------------------------------------------------------
    # Local File
    # --------------------------------------------------------

    else:

        print(
            "Detected local file."
        )


        print(
            "Converting to WAV..."
        )


        wav_path = (
            convert_to_wav(
                source
            )
        )


    # --------------------------------------------------------
    # Chunk Audio
    # --------------------------------------------------------

    print(
        "Chunking audio..."
    )


    chunks = chunk_audio(
        wav_path
    )


    print(
        f"Audio ready — "
        f"{len(chunks)} chunk(s) created."
    )


    return chunks