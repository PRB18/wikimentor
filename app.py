import streamlit as st
from modules.wiki_fetcher import fetch_topic_summary, fetch_wikibooks_links, fetch_wikidata_facts, fetch_wikiversity_resources
from modules.ai_engine import mentor_chat_response, generate_flashcards

st.set_page_config(page_title="WikiMentor", page_icon="📚", layout="wide")

# Theme Styles
mode = st.sidebar.radio("🌗 Theme Mode", ["Light", "Dark"], index=0)

if mode == "Light":
    st.markdown("""
    <style>
        .stApp {
            background-color: #ffffff;
            color: #000000;
        }
        .flashcard {
            background-color: #f0f2f6;
            color: #000;
        }
        .banner p, .banner h1 {
            color: #000000;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .stApp {
            background-color: #111827;
            color: #f3f4f6;
        }
        .flashcard {
            background-color: #1f2937;
            color: #f9fafb;
        }
        .banner p, .banner h1 {
            color: #f3f4f6;
        }
    </style>
    """, unsafe_allow_html=True)

# App Title
st.markdown("""
<div class="banner">
    <h1>🎓 WikiMentor</h1>
    <p>Your AI-Powered Smart Learning Companion</p>
</div>
""", unsafe_allow_html=True)

# Session states
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []

# Sidebar Navigation
menu = st.sidebar.selectbox("📌 Navigate", ["🏫 Learn a Topic", "💬 Mentor Chat", "🗂️ Flashcard Review"])

if menu == "🏫 Learn a Topic":
    st.subheader("📘 Learn a New Topic")
    topic = st.text_input("🔍 Enter a topic to learn:")

    if topic:
        with st.spinner("📚 Fetching summary from Wikipedia..."):
            summary = fetch_topic_summary(topic)

        if summary:
            st.success("Summary fetched successfully!")
            st.markdown("### 📖 Topic Summary")
            st.info(summary)

            st.markdown("### 🔗 Additional Learning Resources")

            with st.spinner("📚 Fetching Wikibooks links..."):
                books = fetch_wikibooks_links(topic)
                if books:
                    for title, url in books:
                        st.markdown(f"- 📘 [{title}]({url})")
                else:
                    st.write("No related books found.")

            with st.spinner("🔬 Fetching Wikidata facts..."):
                facts = fetch_wikidata_facts(topic)
                if facts:
                    for fact in facts:
                        st.markdown(f"- 🧠 {fact}")
                else:
                    st.write("No structured facts found.")

            with st.spinner("🎓 Fetching Wikiversity resources..."):
                resources = fetch_wikiversity_resources(topic)
                if resources:
                    for title, link in resources:
                        st.markdown(f"- 🎓 [{title}]({link})")
                else:
                    st.write("No learning resources found.")

            with st.spinner("🗂️ Creating flashcards..."):
                flashcards = generate_flashcards(summary)
                if flashcards:
                    st.session_state.flashcards = flashcards
                    st.success("✅ Flashcards generated! Check the Flashcard Review tab.")
                else:
                    st.warning("⚠️ No flashcards were generated. Try a different topic.")
        else:
            st.error("Couldn't find that topic. Try again with a simpler keyword.")

elif menu == "💬 Mentor Chat":
    st.subheader("💬 Ask Your AI Mentor")
    
    # Voice input removed for Hugging Face compatibility
    user_query = st.text_input("Type your question:")

    if st.button("🧠 Get Answer") and user_query:
        with st.spinner("Thinking like a mentor..."):
            reply = mentor_chat_response(user_query)
        st.session_state.chat_history.append((user_query, reply))

    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### 📝 Previous Mentor Answers")
        for q, a in reversed(st.session_state.chat_history):
            with st.expander(f"❓ {q}"):
                st.markdown(f"✅ {a}")

elif menu == "🗂️ Flashcard Review":
    st.subheader("🗂️ Flashcard Review Mode")
    st.markdown("Use these flashcards to revise and reinforce your memory.")

    if st.session_state.flashcards:
        for idx, fc in enumerate(st.session_state.flashcards):
            st.markdown(f"""
            <div class='flashcard'>
                <strong>Q{idx+1}: {fc['question']}</strong><br><br>
                <details><summary>Show Answer</summary><p>{fc['answer']}</p></details>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Flashcards will appear here after learning a topic.")
