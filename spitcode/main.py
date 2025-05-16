import typer
from spitcode.recorder import run_record

app = typer.Typer()

@app.command()
def record():
    transcript = run_record()
    typer.echo(f"\n🎧 You said:\n{transcript}\n")

if __name__ == "__main__":
    app()

