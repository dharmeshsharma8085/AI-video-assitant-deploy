# app.py

import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

from main import run_pipeline

from core.rag_engine import (
    build_rag_chain,
    ask_question
)

# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =========================
       APP
       ========================= */

    .stApp {
        background: #071225;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background: #071225;
        border-right: 1px solid #263752;
    }

    .sidebar-title {
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
    }

    .sidebar-subtitle {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 3px;
    }


    /* =========================
       HEADINGS
       ========================= */

    h1 {
        letter-spacing: -1px;
    }

    h2 {
        letter-spacing: -0.5px;
    }


    /* =========================
       CONTAINERS
       ========================= */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #0d1b31;
        border: 1px solid #263752;
        border-radius: 14px;
    }


    /* =========================
       METRICS
       ========================= */

    div[data-testid="stMetric"] {
        background: #0d1b31;
        border: 1px solid #263752;
        padding: 16px;
        border-radius: 14px;
    }


    /* =========================
       BUTTONS
       ========================= */

    .stButton > button {
        border-radius: 10px;
        border: 1px solid #5b52e8;
        background: linear-gradient(
            135deg,
            #4f46e5,
            #7c3aed
        );
        color: white;
        font-weight: 600;
        min-height: 42px;
    }

    .stButton > button:hover {
        border-color: #8b5cf6;
    }


    /* =========================
       INPUTS
       ========================= */

    .stTextInput input,
    .stTextArea textarea {
        background: #0d1b31 !important;
        color: white !important;
        border-color: #2b3c58 !important;
        border-radius: 10px !important;
    }


    /* =========================
       FILE UPLOADER
       ========================= */

    [data-testid="stFileUploader"] {
        background: #0d1b31;
        border: 1px dashed #42516c;
        border-radius: 12px;
    }


    /* =========================
       CHAT
       ========================= */

    [data-testid="stChatMessage"] {
        background: #0d1b31;
        border-radius: 12px;
        border: 1px solid #263752;
    }


    /* =========================
       DIVIDER
       ========================= */

    hr {
        border-color: #263752;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "🤖 **AI Video Assistant**"
    )

    st.caption(
        "AI-Powered Video Analysis"
    )

    st.divider()

    selected_page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📄 Transcript",
            "📝 Summary",
            "✅ Action Items",
            "🔑 Key Decisions",
            "❓ Open Questions",
            "💬 Chat with Meeting",
            "⚙️ Settings"
        ]
    )

    st.divider()

    st.success(
        "System operational"
    )


# ============================================================
# HEADER
# ============================================================

header_col, button_col = st.columns(
    [5, 1]
)

with header_col:

    st.title(
        "AI Video Assistant"
    )

    st.caption(
        "Transform videos and lectures into structured AI insights."
    )


with button_col:

    st.write("")

    if st.button(
        "＋ New Analysis",
        use_container_width=True
    ):

        st.session_state.result = None
        st.session_state.chat_history = []

        st.rerun()


# ============================================================
# INPUT SECTION
# ============================================================

with st.container(border=True):

    st.subheader(
        "🎬 Analyze Video / Audio"
    )

    input_type = st.radio(
        "Input source",
        [
            "YouTube URL",
            "Upload File"
        ],
        horizontal=True
    )

    if input_type == "YouTube URL":

        youtube_url = st.text_input(
            "YouTube URL",
            placeholder="https://www.youtube.com/watch?v=..."
        )

        uploaded_file = None

    else:

        uploaded_file = st.file_uploader(
            "Upload audio or video",
            type=[
                "mp3",
                "wav",
                "mp4",
                "m4a",
                "webm",
                "mov",
                "avi",
                "mkv"
            ]
        )

        youtube_url = ""

    language_col, button_col = st.columns(
        [2, 1]
    )

    with language_col:

        language = st.selectbox(
            "Language",
            [
                "english",
                "hinglish"
            ],
            format_func=lambda x: x.title()
        )

    with button_col:

        st.write("")

        analyze_button = st.button(
            "▶ Start Analysis",
            use_container_width=True
        )


# ============================================================
# RUN PIPELINE
# ============================================================

if analyze_button:

    source = None
    temp_path = None

    # --------------------------------------------------------
    # YouTube
    # --------------------------------------------------------

    if input_type == "YouTube URL":

        if not youtube_url.strip():

            st.error(
                "Please enter a YouTube URL."
            )

            st.stop()

        source = youtube_url.strip()


    # --------------------------------------------------------
    # Uploaded file
    # --------------------------------------------------------

    else:

        if uploaded_file is None:

            st.error(
                "Please upload an audio/video file."
            )

            st.stop()

        suffix = os.path.splitext(
            uploaded_file.name
        )[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(
                uploaded_file.getbuffer()
            )

            temp_path = temp_file.name

        source = temp_path


    # --------------------------------------------------------
    # Execute pipeline
    # --------------------------------------------------------

    try:

        with st.status(
            "Running AI Video Analysis...",
            expanded=True
        ):

            st.write(
                "🎵 Processing audio..."
            )

            result = run_pipeline(
                source,
                language
            )

            st.write(
                "📝 Transcription completed."
            )

            st.write(
                "🧠 AI analysis completed."
            )

            st.write(
                "🔎 RAG vector store created."
            )


        st.session_state.result = result

        # New analysis = new chat
        st.session_state.chat_history = []

        st.success(
            "Analysis completed successfully!"
        )

        st.rerun()


    except Exception as e:

        st.error(
            f"Analysis failed: {e}"
        )


    finally:

        if temp_path and os.path.exists(
            temp_path
        ):

            try:

                os.remove(
                    temp_path
                )

            except Exception:
                pass


# ============================================================
# RESULT
# ============================================================

result = st.session_state.result


# ============================================================
# DASHBOARD
# ============================================================

if (
    result is not None
    and selected_page == "🏠 Dashboard"
):

    st.divider()

    st.subheader(
        result["title"]
    )

    st.caption(
        "AI-generated analysis of the selected video."
    )

    st.divider()

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    transcript_words = len(
        result["transcript"].split()
    )

    col1, col2, col3, col4, col5 = st.columns(
        5
    )

    with col1:

        st.metric(
            "📝 Words",
            f"{transcript_words:,}"
        )

    with col2:

        st.metric(
            "🧠 RAG",
            "Ready"
        )

    with col3:

        st.metric(
            "✅ Actions",
            "Extracted"
        )

    with col4:

        st.metric(
            "🔑 Decisions",
            "Extracted"
        )

    with col5:

        st.metric(
            "❓ Questions",
            "Extracted"
        )


    st.write("")


    # --------------------------------------------------------
    # MAIN DASHBOARD
    # --------------------------------------------------------

    left, right = st.columns(
        [1.6, 1]
    )


    # ========================================================
    # LEFT
    # ========================================================

    with left:

        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        with st.container(border=True):

            st.subheader(
                "📋 Summary"
            )

            st.markdown(
                result["summary"]
            )


        st.write("")


        # ----------------------------------------------------
        # ACTION ITEMS
        # ----------------------------------------------------

        with st.container(border=True):

            st.subheader(
                "✅ Action Items"
            )

            st.markdown(
                result["action_items"]
            )


        st.write("")


        # ----------------------------------------------------
        # DECISIONS
        # ----------------------------------------------------

        with st.container(border=True):

            st.subheader(
                "🔑 Key Decisions"
            )

            st.markdown(
                result["key_decisions"]
            )


        st.write("")


        # ----------------------------------------------------
        # QUESTIONS
        # ----------------------------------------------------

        with st.container(border=True):

            st.subheader(
                "❓ Open Questions"
            )

            st.markdown(
                result["open_questions"]
            )


    # ========================================================
    # RIGHT - CHAT
    # ========================================================

    with right:

        with st.container(border=True):

            st.subheader(
                "💬 Chat with Meeting"
            )

            st.caption(
                "Ask questions based only on the transcript."
            )

            st.divider()

            # -----------------------------------------------
            # CHAT HISTORY
            # -----------------------------------------------

            for message in st.session_state.chat_history:

                with st.chat_message(
                    message["role"]
                ):

                    st.write(
                        message["content"]
                    )


            # -----------------------------------------------
            # CHAT INPUT
            # -----------------------------------------------

            question = st.chat_input(
                "Ask about the meeting..."
            )


            if question:

                st.session_state.chat_history.append(
                    {
                        "role": "user",
                        "content": question
                    }
                )


                with st.chat_message(
                    "user"
                ):

                    st.write(
                        question
                    )


                with st.chat_message(
                    "assistant"
                ):

                    with st.spinner(
                        "Thinking..."
                    ):

                        answer = ask_question(
                            result["rag_chain"],
                            question
                        )


                    st.write(
                        answer
                    )


                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

                st.rerun()


# ============================================================
# TRANSCRIPT
# ============================================================

elif (
    result is not None
    and selected_page == "📄 Transcript"
):

    st.title(
        "📄 Transcript"
    )

    st.caption(
        f"{len(result['transcript'].split()):,} words"
    )

    with st.container(border=True):

        st.text_area(
            "Transcript",
            result["transcript"],
            height=650,
            label_visibility="collapsed"
        )


# ============================================================
# SUMMARY
# ============================================================

elif (
    result is not None
    and selected_page == "📝 Summary"
):

    st.title(
        "📝 Summary"
    )

    st.subheader(
        result["title"]
    )

    with st.container(border=True):

        st.markdown(
            result["summary"]
        )


# ============================================================
# ACTION ITEMS
# ============================================================

elif (
    result is not None
    and selected_page == "✅ Action Items"
):

    st.title(
        "✅ Action Items"
    )

    with st.container(border=True):

        st.markdown(
            result["action_items"]
        )


# ============================================================
# KEY DECISIONS
# ============================================================

elif (
    result is not None
    and selected_page == "🔑 Key Decisions"
):

    st.title(
        "🔑 Key Decisions"
    )

    with st.container(border=True):

        st.markdown(
            result["key_decisions"]
        )


# ============================================================
# OPEN QUESTIONS
# ============================================================

elif (
    result is not None
    and selected_page == "❓ Open Questions"
):

    st.title(
        "❓ Open Questions"
    )

    with st.container(border=True):

        st.markdown(
            result["open_questions"]
        )


# ============================================================
# CHAT PAGE
# ============================================================

elif (
    result is not None
    and selected_page == "💬 Chat with Meeting"
):

    st.title(
        "💬 Chat with Your Meeting"
    )

    st.caption(
        "Answers are grounded in the analyzed transcript."
    )

    st.divider()


    for message in st.session_state.chat_history:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )


    question = st.chat_input(
        "Ask something about the meeting..."
    )


    if question:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )


        with st.chat_message(
            "user"
        ):

            st.write(
                question
            )


        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Thinking..."
            ):

                answer = ask_question(
                    result["rag_chain"],
                    question
                )


            st.write(
                answer
            )


        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()


# ============================================================
# SETTINGS
# ============================================================

elif selected_page == "⚙️ Settings":

    st.title(
        "⚙️ Settings"
    )

    st.subheader(
        "AI Stack"
    )

    with st.container(border=True):

        st.write(
            "🎙️ Whisper — English transcription"
        )

        st.write(
            "🇮🇳 Sarvam AI — Hinglish transcription"
        )

        st.write(
            "🧠 OpenAI — AI analysis"
        )

        st.write(
            "🔎 HuggingFace — Embeddings"
        )

        st.write(
            "🗄️ ChromaDB — Vector database"
        )

        st.write(
            "💬 RAG — Meeting Q&A"
        )


    st.subheader(
        "API Status"
    )

    col1, col2 = st.columns(2)


    with col1:

        if os.getenv("OPENAI_API_KEY"):

            st.success(
                "OpenAI API configured"
            )

        else:

            st.error(
                "OpenAI API key missing"
            )


    with col2:

        if os.getenv("SARVAM_API_KEY"):

            st.success(
                "Sarvam API configured"
            )

        else:

            st.error(
                "Sarvam API key missing"
            )


# ============================================================
# NO RESULT
# ============================================================

elif result is None:

    st.divider()

    st.info(
        "🎬 Add a YouTube URL or upload an audio/video file "
        "above to start your analysis."
    )