import json
from pathlib import Path
import requests
import re

# === Paths ===
CODE_PATH = Path("outputs/main_hardened.py")
README_PATH = Path("outputs/README.md")

# === Ollama config ===
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3:14b-q4_K_M"


def load_code():
    return CODE_PATH.read_text(encoding="utf-8")


def build_prompt(code: str) -> str:
    return f"""
You are a senior technical writer and Python engineer.

Your task is to create a professional, well-structured `README.md` for the following FastAPI app.

It must include:
1. Project description
2. Features
3. Installation instructions (with all necessary Python packages based on the code)
4. How to run the app with `uvicorn`
5. Environment variables explanation
6. API documentation to complement the auto-generated Swagger UI
7. Example `curl` requests for all routes
8. License section

Here is the full code:
---
{code}
---
"""


def call_llm(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )
    data = response.json()
    return data.get("response", "").strip()


def remove_think_blocks(text):
    return re.sub(r"<think>[\s\S]*?</think>", "", text, flags=re.MULTILINE)


def main():
    code = load_code()
    prompt = build_prompt(code)
    readme_text = call_llm(prompt)
    readme_text = remove_think_blocks(readme_text)
    README_PATH.write_text(readme_text.strip(), encoding="utf-8")
    print(f"✅ README.md generated at {README_PATH}")


if __name__ == "__main__":
    main()
