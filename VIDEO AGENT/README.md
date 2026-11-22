# Signalroom — AI Video Assistant

Upload an audio or video file, or enter a YouTube link. The app transcribes English speech locally with Whisper, then uses Google Gemini to produce a title, summary, action items, decisions, open questions, and answers grounded in the transcript.

## Setup

From this directory, create and activate a Python virtual environment, then install the dependencies in `Requirements.txt`. Create a local `.env` file containing:

```dotenv
GOOGLE_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.8-flash
```

The `.env` file is ignored by Git. Use a Gemini model available to your API account.

Run the web app with:

```powershell
python -m streamlit run streamlit_app.py
```

The command-line entry point is `python main.py`.

Transcription runs on CPU and can take several minutes for long recordings. Gemini requests require network access and may fail during provider outages or high demand. Transcript text is sent to Gemini for analysis and chat.
