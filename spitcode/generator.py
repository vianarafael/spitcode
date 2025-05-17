from pathlib import Path
import subprocess

TRANSCRIPT_FILE = "session/transcript.txt"
OUTPUT_FILE = "outputs/main.py"

BASE_PROMPT = '''
You are a senior full-stack developer creating a SaaS boilerplate using FastAPI and HTMX.

User story:
{{user_story}}

Required modules:
- Authentication
- Billing
- User management

Constraints:
- FastAPI
- Use SQLite
- Use HTMX templates

Respond ONLY with valid Python code.
Do NOT include <think> or any commentary. Output Python code only.
'''

def build_prompt():
    user_input = Path(TRANSCRIPT_FILE).read_text().strip()
    return BASE_PROMPT.replace("{{user_story}}", user_input)

def run_qwen(prompt):
    print("🧠 Sending to Qwen3...")

    Path("outputs").mkdir(exist_ok=True)
    prompt_file = "outputs/prompt.txt"
    with open(prompt_file, "w") as f:
        f.write(prompt)

    with open(OUTPUT_FILE, "w") as out:
        subprocess.run(["python", "run_qwen.py", prompt_file], stdout=out)

    print(f"✅ Code written to {OUTPUT_FILE}")

if __name__ == "__main__":
    final_prompt = build_prompt()
    run_qwen(final_prompt)
