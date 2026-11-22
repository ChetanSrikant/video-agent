"""Results, downloads and transcript chat for the recording workspace."""
from html import escape

import streamlit as st


REPORT_SECTIONS = (
    ("Summary", "summary"),
    ("Action items", "action_items"),
    ("Key decisions", "key_decisions"),
    ("Open questions", "open_questions"),
)


def render_results(result):
    title = result["title"].strip() or "Untitled recording"
    transcript = result["transcript"]
    word_count = len(transcript.split())
    sections = [f"# {title}"]
    sections.extend(f"## {label}\n\n{result[key]}" for label, key in REPORT_SECTIONS)

    with st.container(key="recording-results"):
        st.html(
            '<header class="brief-heading">'
            '<p class="brief-kicker">Recording brief</p>'
            f'<h2>{escape(title)}</h2>'
            f'<p class="brief-meta">{word_count:,} words in transcript</p>'
            '</header>'
        )
        summary, follow_ups, full_text = st.tabs(["Summary", "Follow-ups", "Transcript"])
        with summary:
            st.markdown(result["summary"])
            st.download_button(
                "Download report", "\n\n".join(sections),
                file_name="video_report.md", mime="text/markdown",
            )
        with follow_ups:
            for label, key in REPORT_SECTIONS[1:]:
                st.subheader(label, anchor=False)
                st.markdown(result[key])
        with full_text:
            st.text_area("Full transcript", transcript, height=280, disabled=True)
            st.download_button(
                "Download transcript", transcript, file_name="transcript.txt", mime="text/plain"
            )

    with st.container(key="transcript-chat"):
        st.subheader("Ask the transcript", anchor=False)
        history = st.session_state.setdefault("messages", [])
        for message in history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # A chat input inside a container stays with its transcript on the page.
        conversation = st.container()
        question = st.chat_input("Ask about this recording")
        if question:
            with conversation:
                with st.chat_message("user"):
                    st.markdown(question)
                with st.chat_message("assistant"):
                    try:
                        with st.spinner("Searching the transcript…"):
                            answer = result["rag_chain"].invoke(question)
                    except Exception:
                        st.error("Chat could not retrieve an answer. Please try again.")
                    else:
                        st.markdown(answer)
                        history.extend([
                            {"role": "user", "content": question},
                            {"role": "assistant", "content": answer},
                        ])
