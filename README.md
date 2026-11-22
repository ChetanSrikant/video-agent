# Signalroom

An AI video assistant that turns a recording into a searchable transcript, a concise brief, action items, decisions, and follow-up questions.

![Signalroom waveform artwork](VIDEO%20AGENT/assets/signal-field.webp)

## What it does

- Accepts an uploaded audio or video file, or a YouTube link.
- Transcribes English speech locally with Whisper.
- Uses Gemini to generate a title, summary, action items, key decisions, and open questions.
- Lets you ask questions grounded in the transcript.
- Exports the report and transcript from a Streamlit interface.

## Run locally

Open the [`VIDEO AGENT`](VIDEO%20AGENT) folder and follow its [setup guide](VIDEO%20AGENT/README.md). Keep your Google API key in a local `.env` file. The repository's `.gitignore` excludes that file, downloaded media, model artifacts, and virtual environments.

Transcription currently runs on CPU. Gemini analysis requires network access and an available model for your API account.
