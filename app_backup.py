
import streamlit as st

from rag_chat import ask_book, conversation_history
from chapter_summarizer import summarize_chapter, chapters

st.set_page_config(
    page_title="Siddhartha AI Tutor",
    page_icon="📚",
    layout="centered"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chapter_summary" not in st.session_state:
    st.session_state.chapter_summary = None

if "selected_summary_chapter" not in st.session_state:
    st.session_state.selected_summary_chapter = None


# LEFT SIDEBAR
with st.sidebar:
    st.title("📚 Siddhartha Tutor")
    st.write("Your personal AI companion for exploring Siddhartha.")

    st.divider()

    st.subheader("📖 Chapter Summaries")

    selected_chapter = st.selectbox(
        "Select a chapter",
        options=list(chapters.keys())
    )

    if st.button("Generate Summary", use_container_width=True):
        with st.spinner("Generating chapter summary..."):
            st.session_state.chapter_summary = summarize_chapter(
                selected_chapter
            )
            st.session_state.selected_summary_chapter = selected_chapter

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        conversation_history.clear()
        st.rerun()

    st.divider()

    st.subheader("About this project")
    st.write("Powered by Python, Streamlit, ChromaDB, Sentence Transformers, and Ollama + Qwen3.")


# MAIN PAGE
st.title("📚 Siddhartha AI Book Tutor")

# Display chapter summary when available
if st.session_state.chapter_summary is not None:

    st.subheader(
        f"📖 {st.session_state.selected_summary_chapter}"
    )

    st.markdown(st.session_state.chapter_summary)

    if st.button("Close Summary"):
        st.session_state.chapter_summary = None
        st.session_state.selected_summary_chapter = None
        st.rerun()

else:
    st.write(
        "Ask questions, explore ideas, and understand the philosophy of Siddhartha."
    )

    if not st.session_state.messages:
        st.info(
            "Welcome! Ask me anything about Siddhartha by Hermann Hesse."
        )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if question := st.chat_input("Ask a question about Siddhartha..."):

        with st.chat_message("user"):
            st.markdown(question)

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_book(question)

            st.markdown(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })
