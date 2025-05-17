import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:14b-q4_K_M"

def call_local_llm(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "system": "You are a senior Python reviewer. Respond clearly and concisely.",
        },
    )
    result = response.json()
    return result["response"].strip()
