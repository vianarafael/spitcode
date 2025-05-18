import json
from pathlib import Path
import requests
import re



MAIN_PATH = Path("outputs/main.py")
REVIEW_JSON = Path("outputs/review_chunks.json")
REWRITTEN_PATH = Path("outputs/main_rewritten.py")


def load_code():
    return MAIN_PATH.read_text(encoding="utf-8")


def load_chunks():
    return json.loads(REVIEW_JSON.read_text(encoding="utf-8"))



OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3:14b-q4_K_M"


def extract_code_blocks(llm_output: str) -> str:
    """Extract Python code from markdown blocks or fallback to full text."""
    # First remove any think tags
    clean = strip_think_tags(llm_output)
    
    # Remove any markdown code block markers
    clean = re.sub(r"```python\n?", "", clean)
    clean = re.sub(r"```\n?", "", clean)
    
    # Remove any remaining markdown formatting
    clean = re.sub(r"`.*?`", "", clean)
    
    # Remove any leading/trailing whitespace and normalize newlines
    clean = clean.strip()
    clean = re.sub(r'\n{3,}', '\n\n', clean)
    
    return clean

def strip_think_tags(text: str) -> str:
    """Remove <think>...</think> blocks and any other XML-like tags"""
    # Remove think tags
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    # Remove any other XML-like tags
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()

def apply_fixes(code: str, chunks: list[dict]) -> str:
    fixes_summary = "\n".join(
        f"- {c['issue']}: {c['fix']}" for c in chunks if c.get("fix")
    )


    prompt = f"""
    You are a senior Python code refactoring expert.

    Here is the original FastAPI code:
    ---
    {code}
    ---

    Apply the following improvements *without removing or simplifying any functionality*:

    - Use bcrypt for password hashing and verification
    - Use os.getenv() to securely load the JWT secret key
    - Explicitly set the JWT algorithm (e.g., "HS256")
    - Add a refresh token system (access + refresh token endpoints)
    - Implement rate limiting using FastAPI middleware (e.g., SlowAPI)
    - Wrap database operations in try/except and return HTTP 500 errors if they fail
    - Use FastAPI's Depends() to inject the database connection
    - Use Pydantic models for input validation (e.g., for user creation)
    - Use logging for important events and errors
    - Do not remove or replace existing routes like /users, /billing, /dashboard
    - Do not mock database logic — keep real sqlite3 queries
    - Preserve and support existing htmx.render() template endpoints
    - Do not generate explanations, markdown code blocks, or <think> tags

    Return ONLY valid Python source code.
    DO NOT explain anything.
    DO NOT use markdown syntax like ```python.
    DO NOT wrap anything in <think> or other tags.

    Output:
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a senior Python code refactoring assistant.\n"
                        "Always return clean, runnable Python source code.\n"
                        "NEVER include markdown formatting like ```python or ```.\n"
                        "NEVER output commentary, explanations, or <think> blocks.\n"
                        "Only return the rewritten source code."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }
    )

    result = response.json()
    if "error" in result:
        raise Exception(f"Ollama API error: {result['error']}")
    if "message" not in result or "content" not in result["message"]:
        raise Exception(f"Unexpected API response: {result}")
    return result["message"]["content"].strip()


def main():
    original_code = load_code()
    review_chunks = load_chunks()
    raw_output = apply_fixes(original_code, review_chunks)
    clean_output = extract_code_blocks(raw_output)
    
    # Additional final cleaning
    clean_output = re.sub(r'^\s*#.*$', '', clean_output, flags=re.MULTILINE)  # Remove comments
    clean_output = re.sub(r'\n{3,}', '\n\n', clean_output)  # Normalize newlines
    clean_output = clean_output.strip()
    
    REWRITTEN_PATH.write_text(clean_output, encoding="utf-8")
    print(f"✅ Rewritten file saved to {REWRITTEN_PATH}")


if __name__ == "__main__":
    main()
