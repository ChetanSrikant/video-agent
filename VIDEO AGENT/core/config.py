"""Shared runtime configuration for the video assistant."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

def gemini_model():
    return os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
