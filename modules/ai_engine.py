import os
import re
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def call_groq(prompt, system="You are a helpful and concise AI tutor."):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    try:
        res = requests.post(GROQ_URL, headers=HEADERS, json=payload)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"]
        else:
            print("Groq API error:", res.text)
            return "⚠️ Groq API error. Check key or model name."
    except Exception as e:
        print("Request failed:", e)
        return "⚠️ Connection error."

@st.cache_data(show_spinner=False)
def mentor_chat_response(query):
    prompt = f"Explain this concept clearly in simple terms:\n\n{query}"
    return call_groq(prompt)

@st.cache_data(show_spinner=False)
def generate_flashcards(text):
    if len(text) > 2000:
        text = text[:2000]
    prompt = f"""Create 5 flashcards based on this content:\n\n{text}\n\nFormat:\nQ: ...\nA: ..."""
    raw = call_groq(prompt)

    print("🧠 RAW FLASHCARD RESPONSE:\n", raw)  # For debugging

    cards = []
    blocks = re.split(r"Q:\s*", raw)[1:]  # split by Q:
    for block in blocks:
        parts = block.strip().split("A:")
        if len(parts) == 2:
            q = parts[0].strip()
            a = parts[1].strip().split("\n")[0]
            cards.append({"question": q, "answer": a})
    return cards
