
import streamlit as st
import html

from rag_chat import ask_book, conversation_history
from chapter_summarizer import summarize_chapter, chapters
from book_reader import get_chapter_names, get_chapter_pages, get_page

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Siddhartha | AI Reading Companion",
    page_icon="📚",
    layout="wide"
)



# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>

/* Wider reading area */
.block-container {
    max-width: 1450px !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
}

/* Reading notification */
.reader-tip {
    background-color: #EFE5D6;
    border: 1px solid #C9B69F;
    border-left: 5px solid #79583F;
    border-radius: 10px;
    padding: 18px 22px;
    color: #493526 !important;
    margin-top: 15px;
}

.reader-tip strong {
    color: #493526 !important;
    font-size: 16px;
}

.reader-tip p {
    color: #796B5C !important;
    font-size: 14px;
    margin-bottom: 0;
}

/* Better reading typography */
..reader-content {
    color: #493526;
    font-family: Georgia, serif;
    font-size: 16px;
    line-height: 1.8;
    white-space: pre-wrap;
    overflow-wrap: anywhere;

    width: 100% !important;
    max-width: none !important;
    box-sizing: border-box;
}

.reader-paper {
    background-color: #EFE5D6;
    border: 1px solid #C9B69F;
    border-radius: 12px;
    padding: 35px 55px;

    width: 100%;
    box-sizing: border-box;
}



/* Application background */
.stApp {
    background-color: #F7F2E8 !important;
    color: #493526 !important;
}

/* Main content */
.block-container {
    max-width: 1200px;
    padding-top: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #EDE3D3 !important;
}

section[data-testid="stSidebar"] * {
    color: #493526 !important;
}

/* Headings */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {
    color: #493526 !important;
    font-family: Georgia, serif;
}

/* All normal text and Markdown */
.stApp p,
.stApp li,
.stApp strong,
.stApp em,
.stApp blockquote,
.stApp label {
    color: #493526 !important;
}

/* Chapter cards */
.chapter-card,
.book-card {
    background-color: #EFE5D6 !important;
    color: #493526 !important;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #DFD0BC;
    margin-bottom: 15px;
    overflow-wrap: anywhere;
}

.chapter-card * ,
.book-card * {
    color: #493526 !important;
}

/* Dropdown */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #EFE5D6 !important;
    color: #493526 !important;
}

/* Buttons */
.stButton > button {
    background-color: #79583F !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
}

.stButton > button p {
    color: white !important;
}

/* Chat message background */
[data-testid="stChatMessage"] {
    background-color: #EFE5D6 !important;
    border-radius: 12px;
    padding: 15px;
}

/* Chat message text */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] strong {
    color: #493526 !important;
}

/* Chat input container */
[data-testid="stChatInput"] {
    background-color: #EFE5D6 !important;
    border: 1px solid #C9B69F !important;
    border-radius: 12px !important;
}

/* Chat typing area */
[data-testid="stChatInput"] textarea {
    background-color: #EFE5D6 !important;
    color: #493526 !important;
    -webkit-text-fill-color: #493526 !important;
    caret-color: #493526 !important;
}

/* Chat placeholder */
[data-testid="stChatInput"] textarea::placeholder {
    color: #897865 !important;
    -webkit-text-fill-color: #897865 !important;
    opacity: 1 !important;
}

/* Chat input button */
[data-testid="stChatInput"] button {
    background-color: #79583F !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)




# --------------------------------------------------
# CHAPTER DESCRIPTIONS
# --------------------------------------------------

chapter_descriptions = {
    "The Brahmin's Son":
        "Siddhartha grows up surrounded by religious teachings "
        "and rituals, but feels an inner restlessness. He decides "
        "to leave his home and seek spiritual truth.",

    "With the Samanas":
        "Siddhartha joins wandering ascetics and practices "
        "self-denial, fasting and meditation. Yet he continues "
        "questioning whether these practices can lead him to truth.",

    "Gotama":
        "Siddhartha meets the Buddha, Gotama, and listens to "
        "his teachings. Although he respects the Buddha, he "
        "decides to continue his own search.",

    "Awakening":
        "After leaving Govinda and the Buddha's teachings, "
        "Siddhartha begins to experience the world with fresh "
        "eyes and takes responsibility for his own journey.",

    "Kamala":
        "Siddhartha enters the world of love and worldly life. "
        "He meets Kamala and begins learning about relationships, "
        "wealth and pleasure.",

    "Sansara":
        "Siddhartha becomes absorbed in wealth, business and "
        "worldly pleasures. Over time, he feels increasingly "
        "empty and dissatisfied with his life.",

    "The Ferryman":
        "Siddhartha returns to the river and meets the ferryman "
        "Vasudeva. Through listening and observing the river, "
        "he begins discovering a different kind of wisdom.",

    "The Son":
        "Siddhartha experiences the challenges of fatherhood "
        "and struggles with his attachment to his son.",

    "Om":
        "Siddhartha faces deep suffering and eventually finds "
        "a new understanding through the river and the sound Om.",

    "Govinda":
        "Siddhartha reunites with Govinda. Their final conversation "
        "explores wisdom, love and the limits of intellectual teaching."
}


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chapter_summary" not in st.session_state:
    st.session_state.chapter_summary = None

if "summary_chapter" not in st.session_state:
    st.session_state.summary_chapter = None

if "reader_chapter" not in st.session_state:
    st.session_state.reader_chapter = "The Brahmin's Son"

if "reader_page" not in st.session_state:
    st.session_state.reader_page = 1

if "reader_summary" not in st.session_state:
    st.session_state.reader_summary = None

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:

    st.title("📚 Sourav's Reading Room")

    st.caption("A place to explore stories and ideas.")

    st.divider()

    page = st.radio(
        "Explore",
        [
            "Read Siddhartha",
            "Discover Books",
            "AI Book Chat"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.caption("CURRENTLY READING")

    st.markdown("### Siddhartha")
    st.caption("Hermann Hesse")

    st.divider()

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        conversation_history.clear()
        st.rerun()



# --------------------------------------------------
# PAGE 1: READ SIDDHARTHA
# --------------------------------------------------

if page == "Read Siddhartha":

    st.title("📖 Your Reading Room")
    st.caption("Take your time. Read, reflect and discover.")

    st.divider()

    # Get all available chapters
    chapter_names = get_chapter_names()

    # Chapter selection
    selected_chapter = st.selectbox(
        "Choose a chapter",
        options=chapter_names,
        index=chapter_names.index(st.session_state.reader_chapter)
    )

    # Reset page when a different chapter is selected
    if selected_chapter != st.session_state.reader_chapter:
        st.session_state.reader_chapter = selected_chapter
        st.session_state.reader_page = 1
        st.session_state.chapter_summary = None
        st.rerun()

    # Get pages of the selected chapter
    chapter_pages = get_chapter_pages(selected_chapter)

    total_pages = len(chapter_pages)

    # Safety check
    if total_pages == 0:
        st.warning("No readable pages found in this chapter.")

    else:

        # Make sure page number is valid
        current_page = st.session_state.reader_page

        if current_page > total_pages:
            current_page = 1
            st.session_state.reader_page = 1

        # Retrieve current page
        page_data = get_page(
            selected_chapter,
            current_page
        )

        # Chapter heading
        
        page_content = html.escape(page_data["content"])

        st.html(f"""
<div class="reader-paper">
    <h2 style="
        text-align: center;
        color: #493526;
        font-family: Georgia, serif;
    ">
        {html.escape(selected_chapter)}
    </h2>

    <hr style="border: 1px solid #C9B69F;">

    <div class="reader-content">
        {page_content}
    </div>

    <p style="
        text-align: right;
        color: #796B5C;
        font-size: 12px;
    ">
        PDF Page {page_data["pdf_page"]}
    </p>
</div>
""")


        st.write("")

        # Previous and Next navigation
        previous_col, page_col, next_col = st.columns([1, 2, 1])

        with previous_col:

            if st.button(
                "← Previous",
                disabled=current_page == 1,
                use_container_width=True
            ):

                st.session_state.reader_page -= 1
                st.rerun()

        with page_col:

            st.markdown(
                f"<p style='text-align:center; "
                f"color:#79583F; padding-top:8px;'>"
                f"{current_page} / {total_pages}"
                f"</p>",
                unsafe_allow_html=True
            )

        with next_col:

            if st.button(
                "Next →",
                disabled=current_page == total_pages,
                use_container_width=True
            ):

                st.session_state.reader_page += 1
                st.rerun()

        st.divider()

        # Chapter summary
        with st.expander("📚 Generate chapter summary"):

            if st.button("Generate Summary"):

                with st.spinner("Preparing your chapter summary..."):

                    st.session_state.chapter_summary = (
                        summarize_chapter(selected_chapter)
                    )

                    st.session_state.summary_chapter = selected_chapter

            if (
                st.session_state.chapter_summary
                and st.session_state.summary_chapter == selected_chapter
            ):

                st.markdown(
                    st.session_state.chapter_summary
                )

        
        # AI tutor shortcut
        st.markdown("""
        <div class="reader-tip">
            <strong>💬 Need help understanding this chapter?</strong>
            <p>
                Visit AI Book Chat to discuss the characters,
                events and ideas you just read.
            </p>
        </div>
        """, unsafe_allow_html=True)




# --------------------------------------------------
# PAGE 2: DISCOVER BOOKS
# --------------------------------------------------

elif page == "Discover Books":

    st.title("Discover Your Next Read")

    st.caption(
        "Explore books that challenge your thinking "
        "and introduce you to new ideas."
    )

    st.divider()

    st.subheader("Popular books")

    books = [
        {
            "title": "The Alchemist",
            "author": "Paulo Coelho",
            "isbn": "9780062315007",
            "genre": "Philosophical Fiction",
            "description": "A journey about dreams, purpose and discovering your personal legend."
        },
        {
            "title": "1984",
            "author": "George Orwell",
            "isbn": "9780451524935",
            "genre": "Dystopian Fiction",
            "description": "A powerful story about surveillance, freedom and control."
        },
        {
            "title": "Crime and Punishment",
            "author": "Fyodor Dostoevsky",
            "isbn": "9780143058144",
            "genre": "Psychological Fiction",
            "description": "An exploration of morality, guilt and the human mind."
        },
        {
            "title": "Atomic Habits",
            "author": "James Clear",
            "isbn": "9780735211292",
            "genre": "Personal Development",
            "description": "A practical guide to building better habits through small changes."
        }
    ]

    columns = st.columns(4)

    for index, book in enumerate(books):

        with columns[index]:

            st.image(
                f"https://covers.openlibrary.org/b/isbn/{book['isbn']}-L.jpg",
                use_container_width=True
            )

            st.markdown(f"**{book['title']}**")
            st.caption(book["author"])
            st.caption(book["genre"])

            st.write(book["description"])

    st.divider()

    st.subheader("Explore genres")

    genres = [
        "📖 Philosophy",
        "🏛️ Classic Literature",
        "🧠 Psychology",
        "🚀 Science Fiction",
        "❤️ Romance",
        "🔍 Mystery & Thriller",
        "🌱 Self Development",
        "🌍 History"
    ]

    genre_columns = st.columns(4)

    for index, genre in enumerate(genres):

        with genre_columns[index % 4]:
            st.markdown(
                f'<div class="book-card">{genre}</div>',
                unsafe_allow_html=True
            )

    st.divider()

    st.subheader("Authors worth discovering")

    authors = [
        ("Hermann Hesse", "Siddhartha, Steppenwolf"),
        ("Fyodor Dostoevsky", "The Brothers Karamazov, Crime and Punishment"),
        ("Franz Kafka", "The Metamorphosis, The Trial"),
        ("George Orwell", "1984, Animal Farm"),
        ("Paulo Coelho", "The Alchemist, Brida"),
        ("Leo Tolstoy", "War and Peace, Anna Karenina")
    ]

    author_columns = st.columns(3)

    for index, (author, works) in enumerate(authors):

        with author_columns[index % 3]:

            st.markdown(
                f"""
                <div class="book-card">
                    <h4>{author}</h4>
                    <p class="small-text">{works}</p>
                </div>
                """,
                unsafe_allow_html=True
            )


# --------------------------------------------------
# PAGE 3: AI BOOK CHAT
# --------------------------------------------------

elif page == "AI Book Chat":

    st.title("Talk to Siddhartha")

    st.caption(
        "Ask questions about the book and explore "
        "its characters, ideas and philosophy."
    )

    st.divider()

    if not st.session_state.messages:

        st.markdown(
        '<p style="color: #D4A72C; font-size: 17px;">'
        'Welcome! Ask me anything about Siddhartha.'
        '</p>',
        unsafe_allow_html=True
    )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if question := st.chat_input(
        "Ask something about Siddhartha..."
    ):

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):
                answer = ask_book(question)

            st.markdown(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })
