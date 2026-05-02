# 🕵️‍♂️ AI Root Cause Analyzer

Welcome to the **AI Root Cause Analyzer**! If you've ever dealt with a 3 AM system outage and spent hours digging through logs to find the "needle in the haystack," this project is built for you. 

This tool intelligently automates the most painful part of Site Reliability Engineering (SRE): **identifying what broke and how to fix it**. By combining **Vector Databases (ChromaDB)** with **local Large Language Models (Ollama)**, it creates an end-to-end Retrieval-Augmented Generation (RAG) pipeline that learns from your historical incidents to instantly diagnose new ones.

---

## 🌟 Why We Built This

Let's face it, debugging production systems is stressful. When a new error occurs, the solution often lies buried in an incident response from six months ago. We wanted to build a system that acts like your most experienced Senior Engineer—one who never forgets a past outage and can instantly tell you:
1. What the current error means.
2. When something similar happened before.
3. How you fixed it last time.

By running entirely **locally** via Ollama, your sensitive logs and incident data never leave your environment.

---

## 🏗️ Architecture

At its core, this project leverages a RAG (Retrieval-Augmented Generation) pipeline:
1. **Ingestion**: We take historical incident reports, convert them into vector embeddings, and store them securely in a local ChromaDB instance.
2. **Similarity Search**: When a new error occurs, we embed the error message and query ChromaDB for the most contextually similar past incidents.
3. **Generation**: We pass the new error alongside the historical context to a local LLM (`llama3.2`), which generates a clear, concise Root Cause Analysis (RCA) and proposes a fix.

---

## 🚀 Getting Started

Follow these steps to spin up the analyzer on your machine!

### Prerequisites

1. **Python 3.10+**
2. **[Ollama](https://ollama.ai/)** installed and running locally.
3. Pull the required models in Ollama:
   ```bash
   ollama pull nomic-embed-text
   ollama pull llama3.2
   ```

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-root-cause-analyzer.git
   cd ai-root-cause-analyzer
   ```

2. **Activate the virtual environment (recommended):**
   ```bash
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   *(Ensure you have `chromadb`, `ollama`, and Jupyter installed in your environment)*
   ```bash
   pip install chromadb ollama jupyter
   ```

---

## 📚 Notebooks Walkthrough

To see the system in action, run the Jupyter notebooks in the `notebooks/` directory sequentially. They walk you through the entire process step-by-step:

- **`01_ingest_logs.ipynb`**: Embeds and stores fake historical IT incidents into ChromaDB.
- **`02_similarity_search.ipynb`**: Simulates a new error and queries ChromaDB for the nearest matching past incident.
- **`03_root_cause_llm.ipynb`**: Demonstrates generating an RCA purely via LLM passing manual context.
- **`04_final_system.ipynb`**: The grand finale! Combines all steps into a seamless pipeline that takes a system name and error, retrieves context, and outputs a complete diagnostic report.

*Tip: You can re-generate the latter notebooks at any time using `python generate_notebooks.py`.*

---

## 🤝 Contributing

We'd love your help in making this even better! Whether it's adding support for different vector databases, improving the RAG prompt, or expanding the simulated dataset, feel free to open an issue or submit a PR.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

*Made with ❤️ for engineers who prefer sleeping over debugging.*

