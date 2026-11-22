"""Run with python -m streamlit run streamlit_app.py."""
import base64
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit

import streamlit as st
from dotenv import load_dotenv

from ui_results import render_results

APP_DIR = Path(__file__).resolve().parent
load_dotenv(APP_DIR / ".env")
os.chdir(APP_DIR)  # Audio and vector modules use project-relative paths.
MEDIA_TYPES = ["mp4", "mov", "mkv", "webm", "avi", "mp3", "wav", "m4a", "ogg", "flac"]
YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be", "www.youtu.be"}


@st.cache_data(show_spinner=False)
def encoded_art(path, modified):
    return base64.b64encode(path.read_bytes()).decode("ascii")


def process_recording(upload, url):
    from main import run_pipeline

    if upload is None:
        return run_pipeline(url)
    with TemporaryDirectory(prefix="video_agent_") as directory:
        path = Path(directory) / ("upload" + Path(upload.name).suffix.lower())
        path.write_bytes(upload.getbuffer())
        return run_pipeline(str(path))


def source_panel():
    st.html('<h2 class="panel-title">Add a recording</h2>')
    source = st.radio("Recording source", ["File upload", "YouTube link"], horizontal=True,
                      label_visibility="collapsed", key="source-choice")
    upload = None
    url = ""
    if source == "File upload":
        upload = st.file_uploader("Choose an audio or video file", type=MEDIA_TYPES, key="media",
                                  label_visibility="collapsed")
    else:
        url = st.text_input("YouTube video URL", placeholder="https://www.youtube.com/watch?v=…").strip()
    if not st.button("Analyze recording", key="analyze", type="primary", icon=":material/arrow_forward:"):
        return
    if source == "File upload" and upload is None:
        st.warning("Choose an audio or video file first.")
        return
    if source == "YouTube link":
        try:
            parts = urlsplit(url)
            valid_url = parts.scheme in {"http", "https"} and parts.hostname in YOUTUBE_HOSTS
        except ValueError:
            valid_url = False
        if not valid_url:
            st.warning("Enter a valid YouTube video link.")
            return
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("Add GOOGLE_API_KEY to the project's .env file to enable analysis.")
        return
    try:
        with st.spinner("Transcribing your recording and preparing the report…"):
            result = process_recording(upload, url)
    except Exception as error:
        st.error(f"Processing failed: {error}")
        return
    st.session_state.result = result
    st.session_state.messages = []
    st.rerun()


st.set_page_config(page_title="Signalroom · AI Video Assistant", page_icon=":material/graphic_eq:", layout="wide")
stylesheet = (APP_DIR / "assets" / "studio.css").read_text(encoding="utf-8-sig")
st.html(f"<style>{stylesheet}</style>")
st.session_state.setdefault("result", None)
st.html('''<div class="masthead"><div class="brand"><span class="brand-icon" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span>Signalroom</div>
<div class="workspace"><span aria-hidden="true"></span>Local workspace</div></div>''')

if st.session_state.result is None:
    art = APP_DIR / "assets" / "signal-field.webp"
    artwork = encoded_art(art, art.stat().st_mtime_ns)
    st.html(f'''<section class="studio-hero"><img class="field-art" src="data:image/webp;base64,{artwork}" alt="" />
    <div class="hero-copy"><div class="eyebrow"><b></b>AI video assistant</div>
    <h1>Recording <em>studio.</em></h1>
    <p>Turn a recording into a transcript, a concise brief,<br class="desktop-break"> and answers you can explore.</p></div></section>''')
    source_col, detail_col = st.columns([1.65, 1], gap="medium")
    with source_col, st.container(key="source-panel"):
        source_panel()
    with detail_col, st.container(key="session-panel"):
        st.html('''<div class="session-head"><span class="detail-icon" aria-hidden="true">≋</span><h2 class="panel-title">Session details</h2></div>
        <dl class="details"><div><dt>Speech language</dt><dd>English</dd></div><div><dt>Transcription</dt><dd>On device</dd></div>
        <div><dt>Analysis &amp; chat</dt><dd>Google Gemini</dd></div></dl>
        <p class="privacy">Transcript text is shared with Gemini for analysis and chat. Longer recordings take more time.</p>''')
else:
    if st.button("New recording", icon=":material/add:"):
        st.session_state.result = None
        st.session_state.messages = []
        st.rerun()
    render_results(st.session_state.result)
