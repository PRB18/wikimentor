import gradio as gr
import os # Keep os import in case it's used elsewhere, though not for Streamlit env vars now

# Import your existing modules
from modules.wiki_fetcher import fetch_topic_summary, fetch_wikibooks_links, fetch_wikidata_facts, fetch_wikiversity_resources
from modules.ai_engine import mentor_chat_response, generate_flashcards

# --- Gradio Theme and Global Styling ---
# Gradio handles light/dark mode automatically with its themes.
# We'll use a theme that generally looks good. You can experiment with others like
# gr.themes.Default(), gr.themes.Monochrome(), gr.themes.Glass()
theme = gr.themes.Soft()

# Custom CSS for the flashcards to mimic the Streamlit look
# Gradio's theming will handle the overall app background/text colors.
custom_css = """
/* Basic styling for the banner */
.banner {
    text-align: center;
    padding: 20px;
    background-color: var(--background-fill-primary); /* Gradio's primary background color */
    color: var(--text-color-body); /* Gradio's body text color */
    border-radius: var(--radius-xl);
    margin-bottom: 20px;
}
.banner h1 {
    font-size: 2.5em;
    margin-bottom: 0.2em;
    color: var(--text-color-body);
}
.banner p {
    font-size: 1.1em;
    color: var(--text-color-subdued);
}
/* Styling for flashcards, adapting to Gradio's theme variables */
.flashcard {
    background-color: var(--background-fill-secondary); /* Gradio's secondary background color */
    padding: 1em;
    margin-bottom: 1em;
    border-radius: var(--radius-xl);
    border: 1px solid var(--border-color-primary);
    box-shadow: var(--shadow-drop-lg);
}
.flashcard h4 {
    color: var(--text-color-body);
    margin-top: 0;
    margin-bottom: 0.5em;
}
.flashcard details {
    margin-top: 0.5em;
}
.flashcard summary {
    color: var(--text-color-subdued);
    cursor: pointer;
    font-weight: bold;
}
.flashcard p {
    color: var(--text-color-subdued);
    padding-top: 0.5em;
    margin-bottom: 0;
}
"""

# --- Functions to handle logic for Gradio UI interactions ---

def learn_topic_action(topic):
    """
    Handles the logic for the 'Learn a Topic' tab.
    Fetches summary, links, facts, resources, and generates flashcards.
    Returns multiple outputs for Gradio components.
    """
    summary_output = ""
    books_output = ""
    facts_output = ""
    resources_output = ""
    flashcard_status = ""
    flashcards_data = [] # Data to be stored in session state

    if not topic:
        # Return empty strings for outputs and a message for status
        return "", "", "", "", "Please enter a topic to learn.", []

    # Fetch summary
    # Gradio handles loading indicators automatically when functions are running
    summary = fetch_topic_summary(topic)
    if summary:
        summary_output = f"### 📖 Topic Summary\n\n{summary}"
    else:
        summary_output = "Couldn't find that topic. Try again with a simpler keyword."
        # If summary fails, no other data can be fetched, so return early
        return summary_output, "", "", "", "", []

    # Fetch Wikibooks links
    books = fetch_wikibooks_links(topic)
    if books:
        books_output = "### 🔗 Wikibooks Links\n\n" + "\n".join([f"- 📘 [{title}]({url})" for title, url in books])
    else:
        books_output = "No related books found on Wikibooks."

    # Fetch Wikidata facts
    facts = fetch_wikidata_facts(topic)
    if facts:
        facts_output = "### 🔬 Wikidata Facts\n\n" + "\n".join([f"- � {fact}" for fact in facts])
    else:
        facts_output = "No structured facts found on Wikidata."

    # Fetch Wikiversity resources
    resources = fetch_wikiversity_resources(topic)
    if resources:
        resources_output = "### 🎓 Wikiversity Resources\n\n" + "\n".join([f"- 🎓 [{title}]({link})" for title, link in resources])
    else:
        resources_output = "No learning resources found on Wikiversity."

    # Generate flashcards
    flashcards = generate_flashcards(summary)
    if flashcards:
        flashcards_data = flashcards # Store for session state
        flashcard_status = "✅ Flashcards generated! Check the Flashcard Review tab."
    else:
        flashcard_status = "⚠️ No flashcards were generated. Try a different topic."

    return summary_output, books_output, facts_output, resources_output, flashcard_status, flashcards_data


def mentor_chat_action(user_query, chat_history):
    """
    Handles the AI Mentor chat functionality.
    Takes user query and current chat history, generates a response, and updates history.
    """
    if not user_query:
        # If query is empty, return current history without modification
        return chat_history, chat_history

    reply = mentor_chat_response(user_query)
    chat_history.append([user_query, reply]) # Gradio Chatbot expects list of [user_msg, bot_msg]
    return chat_history, chat_history # Return updated history for display and state


def flashcard_review_display(flashcards_data):
    """
    Generates HTML for displaying flashcards based on the session state data.
    """
    if not flashcards_data:
        return "<p style='text-align: center; color: var(--text-color-subdued);'>Flashcards will appear here after learning a topic.</p>"

    flashcard_html = ""
    for idx, fc in enumerate(flashcards_data):
        # Apply inline styles for the flashcard to match the Streamlit look
        # These styles are derived from the custom_css block
        flashcard_html += f"""
        <div class='flashcard'>
            <h4>Q{idx+1}: {fc['question']}</h4>
            <details>
                <summary>Show Answer</summary>
                <p>{fc['answer']}</p>
            </details>
        </div>
        """
    return flashcard_html

# --- Gradio UI Layout ---
# Use gr.Blocks for a multi-tab application
with gr.Blocks(theme=theme, title="WikiMentor", css=custom_css) as demo:
    # App Title and Description (mimicking Streamlit's banner)
    gr.HTML("""
    <div class="banner">
        <h1>🎓 WikiMentor</h1>
        <p>Your AI-Powered Smart Learning Companion</p>
    </div>
    """)

    # Persistent state variables for chat history and flashcards
    # These will maintain their values across different tab interactions within a session
    chat_history_state = gr.State([])
    flashcards_state = gr.State([])

    # Main navigation using Gradio Tabs
    with gr.Tabs() as tabs:
        # --- Learn a Topic Tab ---
        with gr.TabItem("🏫 Learn a Topic", id=0):
            gr.Markdown("## 📘 Learn a New Topic")
            topic_input = gr.Textbox(label="🔍 Enter a topic to learn:", placeholder="e.g., Quantum Physics", scale=4)
            learn_button = gr.Button("📚 Fetch Topic Info", scale=1)

            # Output components for the fetched information
            summary_output = gr.Markdown(label="Topic Summary", show_label=False)
            books_output = gr.Markdown(label="Wikibooks Links", show_label=False)
            facts_output = gr.Markdown(label="Wikidata Facts", show_label=False)
            resources_output = gr.Markdown(label="Wikiversity Resources", show_label=False)
            flashcard_status_output = gr.Markdown(label="Flashcard Generation Status", show_label=False)

            # Connect the button click to the learning function
            learn_button.click(
                fn=learn_topic_action,
                inputs=[topic_input],
                outputs=[
                    summary_output,
                    books_output,
                    facts_output,
                    resources_output,
                    flashcard_status_output,
                    flashcards_state # Update the flashcards_state with new data
                ]
            )

        # --- Mentor Chat Tab ---
        with gr.TabItem("💬 Mentor Chat", id=1):
            gr.Markdown("## 💬 Ask Your AI Mentor")
            # Gradio's Chatbot component handles displaying messages
            chatbot = gr.Chatbot(label="Mentor Chat")
            user_query_input = gr.Textbox(label="Type your question:", placeholder="Ask me anything about your topic...")
            send_button = gr.Button("🧠 Get Answer")

            # Connect the send button to the chat function
            # The .then() method is used to clear the input box after sending
            send_button.click(
                fn=mentor_chat_action,
                inputs=[user_query_input, chat_history_state], # Pass user query and current history
                outputs=[chatbot, chat_history_state] # Update chatbot display and history state
            ).then(
                lambda: "", # Function to clear the input
                outputs=[user_query_input]
            )

        # --- Flashcard Review Tab ---
        with gr.TabItem("🗂️ Flashcard Review", id=2):
            gr.Markdown("## 🗂️ Flashcard Review Mode")
            gr.Markdown("Use these flashcards to revise and reinforce your memory.")
            flashcard_display_area = gr.HTML(label="Your Flashcards")

            # This function will be called when the tab is selected to display flashcards
            # The `load` event of the `Blocks` interface can trigger this when the tab changes
            tabs.select(
                fn=flashcard_review_display,
                inputs=[flashcards_state], # Pass the current flashcards data
                outputs=[flashcard_display_area],
                # This ensures the flashcards are updated when the tab is switched to
                # only if the selected tab is the flashcard review tab
                # condition=lambda selected_tab: selected_tab == 2 # This condition can be tricky with tabs.select
            )
            # A simpler way to ensure flashcards are loaded when the tab is first viewed
            # or when the app loads:
            demo.load(
                fn=flashcard_review_display,
                inputs=[flashcards_state],
                outputs=[flashcard_display_area]
            )


# Launch the Gradio application
# server_name="0.0.0.0" and server_port=7860 are crucial for Hugging Face Spaces deployment
demo.launch(server_name="0.0.0.0", server_port=7860)
