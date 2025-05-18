# Spitcode

> From spoken idea to production-ready FastAPI app — powered by local LLMs.

Spitcode is a full pipeline that transforms a **simple spoken idea** into **production-hardened FastAPI code** with a complete `README.md`, error handling, rate limiting, logging, and OpenAPI docs. No cloud. No API keys. All **offline**.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start Ollama with Qwen model
ollama run qwen3:14b-q4_K_M

# Build your first app
python -m spitcode.main build
```

## ✨ Features

* 🎤 **Voice Input**: Record your ideas naturally
* 🤖 **Local LLM**: Powered by Qwen via Ollama
* 🔒 **Security First**: Built-in rate limiting, error handling, and security best practices
* 📝 **Auto-Documentation**: Generates comprehensive README with curl examples
* 🔄 **Code Improvement**: Automatic code analysis and refactoring
* 🛠️ **Production Ready**: Includes middleware, logging, and error handling
* 📚 **OpenAPI Docs**: Automatic API documentation generation

## 🎯 Why Spitcode?

Because ideas are cheap, but building them isn't. Spitcode helps solo devs and startup builders go from *"I want to build an app that does X"* to working backend code in minutes.

And it all runs on your machine. With your models. Your voice. Your ideas.

## 🧠 What It Does

Spitcode is a modular AI pipeline built for:

* **Recording a spoken feature idea**
* **Generating initial FastAPI code**
* **Analyzing and improving structure, security, and style**
* **Hardening the code for production (middleware, secrets, error handling, etc.)**
* **Auto-generating a `README.md` with curl examples and setup**

## 🛠️ Requirements

* Python 3.10+
* [Ollama](https://ollama.com/) with Qwen model
* FFmpeg (for audio processing)
* 8GB+ RAM recommended
* 20GB+ free disk space

## ⚡ Pipeline Overview

| Step  | Command                                                             | Description                                          |
| ----- | ------------------------------------------------------------------- | ---------------------------------------------------- |
| 1.1   | `python -m spitcode.main record "a todo app with auth and billing"` | Records voice and saves transcript.                  |
| 1.2   | `python -m spitcode.main generate`                                  | Generates first `main.py`.                           |
| 2.1   | `python -m analyzer.code_analyzer`                                  | Analyzes code and proposes improvements.             |
| 2.2   | `python -m analyzer.parse_analysis`                                 | Converts feedback into structured JSON.              |
| 3.1   | `python improver/code_improver.py`                                  | Applies structured improvements.                     |
| 3.2   | `python improver/hardener_agent.py`                                 | Adds prod-grade middleware, error handling, logging. |
| 3.3   | `python improver/generate_readme.py`                                | Generates install + usage docs from code.            |
| Final | `python -m spitcode.main build`                                      | Runs all the above in one go.                        |

## 🧪 Example Use Case


> You say:

> "Build a todo app with login, JWT, SQLite, and subscription billing."

Spitcode will generate:

* `main.py` — working FastAPI app
* `main_rewritten.py` — refactored version with improvements
* `main_hardened.py` — final production-ready API
* `README.md` — curl examples, installation, API docs

## 🧬 Architecture

* **Local LLM**: Uses [Qwen](https://huggingface.co/Qwen/Qwen1.5-14B-Chat) via Ollama
* **Voice Input**: Whisper + FFmpeg
* **Analysis**: RAG with your local analyzer
* **Improvement**: Prompt-based refactor with safety guards
* **Harden**: Security best practices (envvars, headers, rate limiting)
* **Documentation**: Auto-generated README with curl samples

## 📁 Output Folder Structure

```bash
outputs/
├── transcript.txt           # What you said
├── main.py                 # First LLM-generated code
├── main_rewritten.py       # Improved/refactored
├── main_hardened.py        # Prod-ready code
├── review_chunks.json      # Improvement suggestions
└── README.md               # Auto-written documentation
```

## 🔧 Troubleshooting

### Common Issues

1. **Ollama not starting**
   - Ensure Ollama is installed and running
   - Check if the Qwen model is downloaded
   - Verify system requirements are met

2. **Audio recording fails**
   - Check FFmpeg installation
   - Verify microphone permissions
   - Ensure audio input device is working

3. **Code generation issues**
   - Clear the outputs directory
   - Check Python version (3.10+ required)
   - Verify all dependencies are installed

## 🗺️ Roadmap

- [ ] Support for multiple LLM backends
- [ ] Web UI for easier interaction
- [ ] Custom template support
- [ ] Database migration generation
- [ ] Test case generation
- [ ] Docker support
- [ ] CI/CD pipeline generation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

