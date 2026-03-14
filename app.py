import streamlit as st
import time
import streamlit.components.v1 as components
import base64
import os

from services.pdf_service import load_pdfs
from rag_engine import create_vector_store, ask_question

st.set_page_config(page_title="AI PDF Knowledge Assistant", layout="wide")

st.title("📚 AI PDF Knowledge Assistant using RAG")
st.write("Ask questions from your uploaded PDFs.")

def is_small_talk(text):
    small_talk_words = [
        "ok", "okay", "thanks", "thank you", "hi", "hello",
        "bye", "goodbye", "cool", "great", "nice"
    ]

    text = text.lower().strip()

    return text in small_talk_words

# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.header("📂 Upload PDFs")

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files:

        st.write("### Uploaded PDF")

        for file in uploaded_files:
            st.write(file.name)

        if st.button("Process PDFs"):

            with st.spinner("Processing PDFs..."):

                docs = load_pdfs(uploaded_files)
                vectorstore = create_vector_store(docs)

                st.session_state.vectorstore = vectorstore

            st.success("PDFs processed successfully!")

# -----------------------------
# SESSION STATE
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# CHAT HISTORY
# -----------------------------

for i, message in enumerate(st.session_state.messages):

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        # -----------------------------
        # USER MESSAGE BUTTONS
        # -----------------------------

        if message["role"] == "user":

            col1, col2, _ = st.columns([1,1,8])

            with col1:
                if st.button("🗑", key=f"delete_{i}"):

                    st.session_state.messages = st.session_state.messages[:i]

                    st.rerun()

            with col2:
                if st.button("✏", key=f"edit_{i}"):

                    st.session_state.edit_index = i
                    st.session_state.edit_text = message["content"]

                    st.rerun()

        # -----------------------------
        # ASSISTANT FEATURES
        # -----------------------------

        if message["role"] == "assistant":

            # COPY BUTTON

            copy_html = f"""
            <div style="display:flex;justify-content:flex-end;margin-top:5px;">
            <button id="copyBtn{i}"
            onclick="
            navigator.clipboard.writeText(`{message['content']}`);
            var btn=document.getElementById('copyBtn{i}');
            btn.innerHTML='✅ Copied';
            setTimeout(function(){{btn.innerHTML='📋 Copy';}},2000);
            "
            style="
            background:#2b2b2b;
            font-size:13px;
            color:white;
            border:1px solid #444;
            padding:4px 10px;
            border-radius:6px;
            cursor:pointer;">
            📋 Copy
            </button>
            </div>
            """

            components.html(copy_html, height=40)

            # SOURCES

            if "sources" in message and message["sources"]:

                st.markdown("### 📚 Sources")

                for source, page in message["sources"]:
                    st.write(f"📄 {source} — Page {page}")

# -----------------------------
# GENERATE AI ANSWER
# -----------------------------

if "pending_question" in st.session_state:

    question = st.session_state.pending_question
    del st.session_state.pending_question

    if is_small_talk(question):

        answer = "😊 You're welcome! If you have more questions about the PDFs, feel free to ask."
        sources = []

    else:

        answer, sources = ask_question(
            st.session_state.vectorstore,
            question
        )

    if answer.strip() == "":
        answer = "⚠ No answer generated."

    # STREAMING RESPONSE
    with st.chat_message("assistant"):

        placeholder = st.empty()
        text = ""

        for char in answer:
            text += char
            placeholder.markdown(text + "▌")
            time.sleep(0.01)

        placeholder.markdown(text)

        copy_html = f"""
        <div style="display:flex;justify-content:flex-end;margin-top:5px;">
        <button id="copyBtn_live"
        onclick="
        navigator.clipboard.writeText(`{text}`);
        var btn=document.getElementById('copyBtn_live');
        btn.innerHTML='✅ Copied';
        setTimeout(function(){{btn.innerHTML='📋 Copy';}},2000);
        "
        style="
        background:#1f2937;
        font-size:13px;
        color:white;
        border:none;
        padding:4px 10px;
        border-radius:6px;
        cursor:pointer;">
        📋 Copy
        </button>
        </div>
        """

        components.html(copy_html, height=40)

        # show sources
        if sources:
            st.markdown("### 📚 Sources")
            for source, page in list(dict.fromkeys(sources)):
                st.write(f"📄 {source} — Page {page}")

    # save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": list(dict.fromkeys(sources))
    })

# -----------------------------
# EDIT QUESTION
# -----------------------------

if "edit_index" in st.session_state:

    new_question = st.text_input(
        "Edit your question:",
        value=st.session_state.edit_text
    )

    if st.button("Update Question"):

        index = st.session_state.edit_index

        # remove messages after edited message
        st.session_state.messages = st.session_state.messages[:index]

        st.session_state.edited_question = new_question

        del st.session_state.edit_index
        del st.session_state.edit_text

        st.rerun()

# -----------------------------
# USER INPUT
# -----------------------------

question = st.chat_input("Ask a question from the PDFs")

if "edited_question" in st.session_state:

    question = st.session_state.edited_question
    del st.session_state.edited_question

# -----------------------------
# NEW QUESTION
# -----------------------------

if question:

    if "vectorstore" not in st.session_state:
        st.warning("⚠ Please upload and process PDFs first.")
        st.stop()

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    st.session_state.pending_question = question

    st.rerun()
