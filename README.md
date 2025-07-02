# 🎓 WikiMentor — AI-Powered Learning Assistant

Welcome to **WikiMentor**, your personalized smart learning companion.  
Search a topic ➤ get concise explanations ➤ review flashcards ➤ ask follow-up questions from a mentor AI.  
All powered by **LLama 3 via GroqCloud** 🧠⚡

---

## 🚀 Features

- 🔍 **Learn a Topic** — Search anything, get:
  - Wikipedia summary
  - Wikibooks resources
  - Wikidata facts
  - Wikiversity links
- 💬 **Mentor Chat** — Ask questions and get clean, simple AI explanations
- 🧠 **Flashcard Review Mode** — Auto-generated flashcards to help you revise
- 🎨 **Dark/Light Mode**
- 🖥️ **Streamlit UI**, fully deployable on Hugging Face Spaces

---

## 🧠 AI Model Used

This app uses:

> 🧠 `llama3-8b-8192` (Meta AI)  
> ⚡ Served via [GroqCloud](https://console.groq.com/)  
> 🔌 Accessed through OpenAI-compatible APIs

---

## 🛠️ Tech Stack

| Layer        | Tech                     |
|--------------|--------------------------|
| 💡 LLM        | Meta’s LLaMA 3 (via Groq) |
| 🧠 Flashcards | LLM Prompt Engineering   |
| 🔍 Knowledge  | Wikipedia, Wikibooks, Wikiversity, Wikidata APIs |
| 🌐 Frontend  | Streamlit                |
| ☁️ Hosting   | Hugging Face Spaces      |

---

## 📦 How to Run Locally

> 💡 Requires Python 3.9+ and `streamlit`

```bash
git clone https://github.com/YOUR_USERNAME/wikimentor.git
cd wikimentor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

🔐 Set your Groq API key (optional for local dev)

export GROQ_API_KEY=your_key_here

▶️ Then run:

streamlit run app.py

🌐 Deploy to Hugging Face Spaces

    Create a new HF Space (SDK: Streamlit)

    Upload:

        app.py

        modules/

        requirements.txt

    Add your GROQ_API_KEY as a secret in Settings > Secrets

Done ✅
📁 Project Structure

wikimentor/
├── app.py
├── requirements.txt
├── modules/
│   ├── ai_engine.py
│   └── wiki_fetcher.py

📝 License

This project is licensed under the MIT License.
Feel free to remix, improve, and build on it 🔥
✨ Author

Built with 💙 by Rishi Babu
Powered by curiosity, caffeine, and Groq 🤖☕⚡
