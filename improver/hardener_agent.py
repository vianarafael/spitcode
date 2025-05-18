import os
import json
from pathlib import Path
import requests
import ast

MAIN_PATH = Path("outputs/main_rewritten.py")
HARDENED_PATH = Path("outputs/main_hardened.py")
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3:14b-q4_K_M"

def load_code():
    return MAIN_PATH.read_text(encoding="utf-8")

def hardening_instructions() -> str:
    return """
You are a senior Python security engineer.
You will harden this FastAPI code for production use by applying the following:

1. Security:
   - Enforce HTTPS or document enforcement instructions
   - Require secrets like JWT keys via os.getenv with no fallbacks
   - Validate and sanitize user inputs (e.g., password, email)
   - Add secure headers using middleware
   - Set strict CORS policies
   - Disable debug mode

2. Logging:
   - Log critical security and failure events

3. Resilience:
   - Use structured exception handling (try/except with HTTPExceptions)
   - Avoid logging sensitive data
   - Fail gracefully if dependencies like DB or secrets are misconfigured

Return ONLY the final Python source code.
DO NOT include markdown, explanations, or tags.
The code must be clean, executable, and production-hardened.
"""

def is_valid_python(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

def call_llm(code: str) -> str:
    messages = [
        {"role": "system", "content": hardening_instructions()},
        {"role": "user", "content": f"Here is the FastAPI code:\n\n{code}\n\nPlease return only hardened Python code."}
    ]

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "messages": messages,
            "stream": False
        }
    )
    result = response.json()
    return result.get("message", {}).get("content", "").strip()

def harden_code(code: str) -> str:
    hardened_code = call_llm(code)
    if is_valid_python(hardened_code):
        return hardened_code
    else:
        print("⚠️ Hardened code failed syntax check. Falling back to original.")
        return code

def main():
    original = load_code()
    hardened = harden_code(original)
    HARDENED_PATH.write_text(hardened, encoding="utf-8")
    print(f"✅ Hardened code written to {HARDENED_PATH}")

if __name__ == "__main__":
    main()
