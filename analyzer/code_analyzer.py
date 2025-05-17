# analyzer/code_analyzer.py
from pathlib import Path
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.query_engine import RetrieverQueryEngine
from analyzer.llm_runner import call_local_llm

# Load docs
docs = SimpleDirectoryReader("analyzer/rag_docs").load_data()

embed_model = HuggingFaceEmbedding(
    model_name="nomic-ai/nomic-embed-text-v1.5",
    embed_batch_size=16,
    trust_remote_code=True,
    device="cpu", # my gpu is not enought for qwe3 and the embed model
)

index = VectorStoreIndex.from_documents(docs, embed_model=embed_model)
retriever = index.as_retriever(similarity_top_k=5)

def analyze_code(code: str) -> str:
    context_docs = retriever.retrieve(code)
    context = "\n\n".join([d.text for d in context_docs])

    prompt = f"""
You are a FastAPI best practices and security expert.

Using the documentation below, analyze the given code.

# Documentation
{context}

# Code
{code}

---

Provide:
1. Best practice violations
2. Security/performance issues
3. Suggestions for modularity & structure
4. A proposed folder layout if needed

Respond with bullet points. No need to restate the code.
"""

    return call_local_llm(prompt)

# Example usage
if __name__ == "__main__":
    code_path = Path("outputs/main.py")
    if not code_path.exists():
        print("❌ No main.py file found to analyze.")
    else:
        print("🧠 Analyzing main.py using Qwen + RAG...")
        analysis = analyze_code(code_path.read_text())
        print("✅ Review complete:\n")
        print(analysis)
