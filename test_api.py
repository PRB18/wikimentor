import requests
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

endpoint = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}
prompt = "Explain photosynthesis in 1 paragraph."

response = requests.post(endpoint, headers=headers, json={"inputs": prompt})
print("Status:", response.status_code)
print("Body:", response.text)
