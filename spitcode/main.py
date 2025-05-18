from pathlib import Path
import typer
import subprocess
from spitcode.recorder import run_record
from spitcode.generator import build_prompt, run_qwen
from analyzer.code_analyzer import analyze_code
from analyzer.parse_analysis import extract_chunks
from improver.code_improver import main as improve_code
from improver.hardener_agent import main as harden_code
from improver.generate_readme import main as generate_readme


app = typer.Typer()

@app.command()
def record():
    transcript = run_record()
    typer.echo(f"\n🎧 You said:\n{transcript}\n")

@app.command()
def generate():
    prompt = build_prompt()
    run_qwen(prompt)

@app.command()
def analyze():
    code_path = Path("outputs/main.py")
    if not code_path.exists():
        typer.echo("❌ No main.py found.")
        raise typer.Exit()

    typer.echo("🧠 Running analysis...")
    review = analyze_code(code_path.read_text())
    Path("outputs/analysis.txt").write_text(review)
    typer.echo("✅ Analysis saved to outputs/analysis.txt")

@app.command()
def build():
    """Full build pipeline: record, generate, analyze, improve, harden, document."""
    # typer.echo("📥 Step 1: Recording use case...")
    # transcript = run_record()
    # typer.echo(f"\n🎧 You said:\n{transcript}\n")

    typer.echo("🛠️  Step 2: Generating initial code...")
    prompt = build_prompt()
    run_qwen(prompt)

    typer.echo("🔎 Step 3: Analyzing code...")
    code_path = Path("outputs/main.py")
    review = analyze_code(code_path.read_text())
    Path("outputs/analysis.txt").write_text(review)

    typer.echo("📊 Step 4: Parsing analysis into review_chunks.json...")
    extract_chunks("outputs/analysis.txt")

    typer.echo("♻️  Step 5: Improving code...")
    improve_code()

    typer.echo("🧱 Step 6: Hardening for production...")
    harden_code()

    typer.echo("📄 Step 7: Generating README.md...")
    generate_readme()

    typer.echo("✅ All steps complete. Check the outputs/ folder.")



if __name__ == "__main__":
    app()

