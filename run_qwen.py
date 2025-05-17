import sys
import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3:14b-q4_K_M"

# Read the prompt file passed as argument
with open(sys.argv[1]) as f:
    prompt = f.read()

# Send prompt to Ollama
response = requests.post(
    OLLAMA_URL,
    json={
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "system": "You are a code generator. DO NOT output <think> tags or internal thoughts. Just code."
    },
    stream=True
)

# Accumulate output here
buffer = ""

for line in response.iter_lines():
    if line:
        try:
            data = json.loads(line)
            token = data.get("response", "")
            if token.strip() in ("```", "python", "text", "json"):
                continue
            buffer += token
        except Exception as e:
            print(f"# ⚠️ Error: {e}", file=sys.stderr)

# Remove <think>...</think> blocks if they slipped through
buffer = re.sub(r"<think>.*?</think>", "", buffer, flags=re.DOTALL)

# Final cleanup: remove stray backticks
buffer = buffer.replace("```", "").strip()

# Output final result
print(buffer)
