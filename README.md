# 🎓 WikiMentor — AI-Powered Learning Assistant

Welcome to **WikiMentor**, your personalized smart learning companion.  
Search a topic ➤ get concise explanations ➤ review flashcards ➤ ask follow-up questions from a mentor AI.  
All powered by **LLama 3 via GroqCloud** 🧠⚡


---

## 🔀 Versions

| Mode              | Stack     | File             | Status |
|-------------------|-----------|------------------|--------|
| 🖥️ Local Dev       | Streamlit | `app.py`         | Full UI (Learn + Chat + Flashcards) |
| 🌐 HF Deployment   | Gradio    | `gradio_app.py`  | Simplified UI for Hugging Face |

👉 Live App: [View on Hugging Face](https://huggingface.co/spaces/Rizzhi/wikimentor)

---

## 🧠 AI Model Used

> 🧠 `llama3-8b-8192` by Meta  
> ⚡ Served via [GroqCloud](https://console.groq.com/)  
> 🔌 Accessed through OpenAI-compatible API

---

## 🚀 Features

- 🔍 **Learn a Topic** — Wikipedia summary + books + facts
- 💬 **Mentor Chat** — Ask follow-up questions
- 🧠 **Flashcard Generator** — Auto-review mode
- 🌗 **Dark/Light Theme (Streamlit version)**

---

## 🛠️ Tech Stack

| Layer        | Tech                     |
|--------------|--------------------------|
| 💡 LLM        | Meta’s LLaMA 3 (via Groq) |
| 🌍 Data APIs  | Wikipedia, Wikibooks, Wikidata, Wikiversity |
| 💬 Frontend  | Streamlit (local), Gradio (cloud) |
| ☁️ Hosting   | Hugging Face Spaces      |

---

## 📁 Project Structure

wikimentor/
├── app.py # Streamlit version
├── gradio_app.py # Gradio HF deploy version
├── requirements.txt
├── modules/
│ ├── ai_engine.py
│ └── wiki_fetcher.py


---

## 💻 How to Run Locally (Streamlit)

```bash
git clone https://github.com/PRB18/wikimentor.git
cd wikimentor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

🌐 How to Deploy to Hugging Face (Gradio)

    Use gradio_app.py as your entrypoint

    Set your GROQ_API_KEY as a secret in HF settings

    Make sure requirements.txt includes:

        gradio

        requests

        wikipedia

📝 License

This project is licensed under the MIT License.
Feel free to remix, improve, and build on it 🔥
✨ Author

Built with 💙 by Rishi Babu
Powered by curiosity, caffeine, and Groq 🤖☕⚡
