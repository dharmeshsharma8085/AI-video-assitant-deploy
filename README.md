🤖 AI Video Assistant

<p align="center">
  <img src="assets/app-screenshot.png" alt="AI Video Assistant Dashboard" width="100%">
</p>

<p align="center">
  <b>AI-powered video and meeting analysis with transcription, RAG, and interactive chat.</b>
</p>

Transform videos, lectures, and meetings into structured AI insights.

🔴 Live Demo: https://g4qt9epskgcw7r2npryh4k.streamlit.app/

Developed by Dharmesh Sharma

🚀 Overview

AI Video Assistant is an AI-powered Streamlit application that converts video/audio content into useful, structured information.

Instead of watching a long video again and again, you can provide a YouTube URL or upload an audio/video file, and the application can:

🎙️ Transcribe the content

📝 Generate an AI-powered summary

✅ Extract action items

🔑 Identify key decisions

❓ Find open questions

💬 Chat with the analyzed meeting/video

🔎 Use RAG to ground answers in the transcript

📄 View and export the generated information

The project is designed as a practical end-to-end AI application, combining speech-to-text, LLMs, embeddings, vector search, and a Streamlit interface.

✨ Features

🎬 Video / Audio Input

Two input methods are supported:

YouTube URL

Uploaded audio/video files

Supported upload formats include:

MP3 · WAV · MP4 · M4A · WEBM · MOV · AVI · MKV

🎙️ Speech-to-Text

The application supports:

🇬🇧 English transcription using OpenAI Whisper

🇮🇳 Hinglish transcription using Sarvam AI

Audio processing is handled with FFmpeg + Pydub.

🧠 AI Analysis

After transcription, the application generates structured insights such as:

📋 Summary

✅ Action Items

🔑 Key Decisions

❓ Open Questions

🏷️ AI-generated title

🔎 RAG-Powered Meeting Chat

The transcript is converted into searchable knowledge using:

Sentence Transformers / Hugging Face embeddings

ChromaDB vector database

LangChain

Retrieval-Augmented Generation (RAG)

Users can ask questions about the analyzed content and receive answers grounded in the transcript.

Example:

"What were the main decisions made in the meeting?"

"Who is responsible for the next action?"

"What questions are still unresolved?"

🖥️ Application Interface

The dashboard provides a clean dark-themed interface with navigation for:

🏠 Dashboard

📄 Transcript

📝 Summary

✅ Action Items

🔑 Key Decisions

❓ Open Questions

💬 Chat with Meeting

⚙️ Settings

🏗️ Architecture

                    ┌─────────────────────┐
                    │   YouTube / Upload  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Audio Extraction  │
                    │    FFmpeg/Pydub     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Speech-to-Text    │
                    │ Whisper / Sarvam AI │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Transcript       │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
      ┌─────────────────┐           ┌─────────────────┐
      │   LLM Analysis  │           │   RAG Pipeline  │
      │     OpenAI      │           │ Embeddings +    │
      │                 │           │ ChromaDB        │
      └────────┬────────┘           └────────┬────────┘
               │                             │
               ▼                             ▼
      ┌─────────────────┐           ┌─────────────────┐
      │ Summary / Tasks │           │ Meeting Chat    │
      │ Decisions / Q&A │           │ Grounded Q&A    │
      └─────────────────┘           └─────────────────┘

🛠️ Tech Stack

Category

Technology

Frontend / UI

Streamlit

Programming Language

Python

Video Download

yt-dlp

Audio Processing

FFmpeg, Pydub

English STT

OpenAI Whisper

Hinglish STT

Sarvam AI

LLM

OpenAI

LLM Framework

LangChain

Embeddings

Hugging Face / Sentence Transformers

Vector Database

ChromaDB

RAG

LangChain + ChromaDB

PDF Generation

ReportLab / FPDF2

Environment Management

python-dotenv

Deployment

Streamlit Community Cloud

📁 Project Structure

AI-video-assitant-deploy/
│
├── app.py
├── main.py
├── requirements.txt
├── packages.txt
│
├── core/
│   ├── transcriber.py
│   ├── summarize.py
│   ├── vector_store.py
│   └── rag_engine.py
│
└── README.md

Project structure may evolve as new features are added.

⚙️ Installation

1. Clone the repository

git clone https://github.com/dharmeshsharma8085/AI-video-assitant-deploy.git
cd AI-video-assitant-deploy

2. Create a virtual environment

python -m venv .venv

3. Activate the environment

Windows:

.venv\Scripts\activate

Linux / macOS:

source .venv/bin/activate

4. Install dependencies

pip install -r requirements.txt

5. Install FFmpeg

Make sure FFmpeg is installed and available in your system PATH.

For Streamlit deployment, the project uses packages.txt to request the FFmpeg system package.

🔐 Environment Variables

Create a .env file for local development:

OPENAI_API_KEY=your_openai_api_key
SARVAM_API_KEY=your_sarvam_api_key

Never commit your .env file or API keys to GitHub.

For cloud deployment, configure the secrets through the deployment platform.

▶️ Run Locally

Start the Streamlit application:

streamlit run app.py

Then open the local Streamlit URL shown in the terminal.

☁️ Deployment

The application is deployed using Streamlit Community Cloud.

Live Application

👉 https://g4qt9epskgcw7r2npryh4k.streamlit.app/

The application can be updated by pushing changes to the connected GitHub repository.

🧪 Example Workflow

1. Open the application
        ↓
2. Paste a YouTube URL
        ↓
3. Select English / Hinglish
        ↓
4. Click "Start Analysis"
        ↓
5. Extract and process audio
        ↓
6. Generate transcript
        ↓
7. Generate AI insights
        ↓
8. Build RAG vector store
        ↓
9. Explore summary, decisions & action items
        ↓
10. Chat with the analyzed content

💡 Why This Project?

Long videos and meetings contain a lot of information, but finding the important parts manually takes time.

This project demonstrates how multiple AI technologies can be combined into one practical workflow:

Audio → Transcription → LLM Analysis → Embeddings → Vector Search → RAG → Interactive Chat

It is also a hands-on implementation of a modern AI application architecture rather than a simple chatbot.

🔮 Future Improvements

Potential improvements include:

⏱️ Timestamp-based transcript navigation

👥 Speaker identification / diarization

📊 Meeting analytics

🌍 More language support

⚡ Faster transcription

💾 Persistent vector storage

🔐 User authentication

📚 Multiple-video knowledge bases

📤 More export formats

🚀 More optimized cloud deployment

👨‍💻 Author

Dharmesh Sharma

AI / ML Developer building practical AI applications with Python, LLMs, RAG, LangChain, and modern deployment tools.

Live Project:
https://g4qt9epskgcw7r2npryh4k.streamlit.app/

GitHub:
https://github.com/dharmeshsharma8085/AI-video-assitant-deploy

⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

📌 Project Status

🟢 Live & Deployed

Built with Python, Streamlit, Whisper, Sarvam AI, OpenAI, LangChain, Hugging Face, and ChromaDB.
