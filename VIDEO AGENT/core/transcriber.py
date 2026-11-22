import whisper
import os
import subprocess
import numpy as np
from imageio_ffmpeg import get_ffmpeg_exe

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

_model = None


def load_model():
    global _model

    if _model is None:
        print("Loading Whisper model...")
        _model = whisper.load_model(WHISPER_MODEL, device="cpu")
        print("Whisper model loaded successfully")

    return _model


def transcribe_chunk(chunk_path: str) -> str:
    if not os.path.isfile(chunk_path) or os.path.getsize(chunk_path) == 0:
        print(f"Skipping missing or empty audio chunk: {chunk_path}")
        return ""

    model = load_model()

    try:
        decoded = subprocess.run(
            [get_ffmpeg_exe(), "-nostdin", "-threads", "0", "-i", chunk_path,
             "-f", "s16le", "-ac", "1", "-acodec", "pcm_s16le", "-ar", "16000", "-"],
            capture_output=True, check=True,
        ).stdout
        audio = np.frombuffer(decoded, dtype=np.int16).astype(np.float32) / 32768.0
        result = model.transcribe(
            audio,
            task="transcribe",
            language="en",
            fp16=False,
        )
    except subprocess.CalledProcessError as error:
        print(f"Skipping unreadable audio chunk {chunk_path}: {error}")
        return ""

    return result.get("text", "").strip()


def transcribe_all(chunks: list[str]) -> str:
    transcribed_chunks = []

    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i+1}")
        text = transcribe_chunk(chunk)
        if text:
            transcribed_chunks.append(text)

    print("Transcription completed")
    return " ".join(transcribed_chunks)