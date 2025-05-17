from pathlib import Path
import typer
from spitcode.recorder import run_record
from spitcode.generator import build_prompt, run_qwen
from analyzer.code_analyzer import analyze_code


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



if __name__ == "__main__":
    app()

