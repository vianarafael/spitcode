import argparse
import subprocess
import sys
from pathlib import Path

TRANSCRIPT_PATH = Path("session/transcript.txt")
MAIN_PATH = Path("outputs/main.py")
REVIEW_PATH = Path("outputs/review.txt")
REVIEW_JSON = Path("outputs/review_chunks.json")
REWRITTEN_PATH = Path("outputs/main_rewritten.py")
README_PATH = Path("outputs/README.md")


def run(cmd: list[str], desc: str):
    print(f"\n🚀 {desc}...")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Failed: {desc}")
        sys.exit(1)


def build(use_case: str):
    run(["python", "-m", "spitcode.main", "record", use_case], "Recording use case")
    run(["python", "-m", "spitcode.main", "generate"], "Generating initial code")
    run(["python", "-m", "analyzer.code_analyzer"], "Analyzing code")
    run(["python", "analyzer/parse_analysis.py"], "Parsing code analysis to JSON")
    run(["python", "improver/code_improver.py"], "Refactoring based on suggestions")
    run(["python", "improver/hardener_agent.py"], "Hardening for production")
    run(["python", "improver/generate_readme.py"], "Generating README")
    print("\n✅ All steps completed. See outputs/ directory.")


def main():
    parser = argparse.ArgumentParser(description="SpitCode CLI")
    subparsers = parser.add_subparsers(dest="command")

    build_parser = subparsers.add_parser("build", help="Build app from natural language")
    build_parser.add_argument("use_case", type=str, help="Use case prompt in quotes")

    args = parser.parse_args()

    if args.command == "build":
        build(args.use_case)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
