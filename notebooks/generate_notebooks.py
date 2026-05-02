import nbformat
import os

def create_notebook(cells_content, output_path):
    nb = nbformat.v4.new_notebook()
    for cell_type, source in cells_content:
        if cell_type == "markdown":
            nb.cells.append(nbformat.v4.new_markdown_cell(source))
        elif cell_type == "code":
            nb.cells.append(nbformat.v4.new_code_cell(source))
    with open(output_path, "w") as f:
        nbformat.write(nb, f)

# 02_similarity_search.ipynb
nb2_cells = [
    ("markdown", "# Step 2: Semantic Similarity Search\nIn this notebook, we'll query the Chroma DB we populated in the first notebook to find similar historical incidents based on a new error log."),
    ("code", "import chromadb\nimport ollama\nimport json\n\nCHROMA_PATH = \"./chroma_db\"\nCOLLECTION_NAME = \"incident_logs\"\nEMBED_MODEL = \"nomic-embed-text\"\n\nclient = chromadb.PersistentClient(path=CHROMA_PATH)\ncollection = client.get_collection(name=COLLECTION_NAME)"),
    ("code", "def get_embedding(text):\n    response = ollama.embeddings(\n        model=EMBED_MODEL,\n        prompt=text\n    )\n    return response[\"embedding\"]"),
    ("markdown", "Let's simulate a new issue occurring in the `payment-service`."),
    ("code", "new_incident = \"\"\"\nSystem: payment-service\nError: DB Connection timed out while trying to process payment\n\"\"\"\n\nprint(\"Searching for similar past incidents...\")\nquery_embedding = get_embedding(new_incident)\n\nresults = collection.query(\n    query_embeddings=[query_embedding],\n    n_results=1\n)\n\nprint(\"\\n--- Top Match ---\")\nfor doc in results['documents'][0]:\n    print(doc)"),
]

# 03_root_cause_llm.ipynb
nb3_cells = [
    ("markdown", "# Step 3: Root Cause Analysis using LLMs\nHere we explore how to pass incident context into a generative LLM (like `llama3`) via Ollama to automatically suggest a root cause and a fix."),
    ("code", "import ollama\n\nLLM_MODEL = \"llama3.2\"\n\ntest_log = \"\"\"\nSystem: auth-service\nError: JWT token validation failed\n\"\"\"\n\nsimilar_incident_context = \"\"\"\nRoot Cause: Expired secret\nFix: Update token secret\n\"\"\"\n\nprompt = f\"\"\"\nYou are an expert Site Reliability Engineer.\nA new incident has occurred:\n{test_log}\n\nHere is a similar historical incident for context:\n{similar_incident_context}\n\nBased on this context, what is the most likely root cause for the new incident, and what fix would you propose? Please be concise.\n\"\"\""),
    ("code", "print(\"Analyzing root cause with LLM...\")\nresponse = ollama.chat(model=LLM_MODEL, messages=[\n  {\n    'role': 'user',\n    'content': prompt\n  }\n])\n\nprint(\"\\n--- LLM Root Cause Analysis ---\")\nprint(response['message']['content'])")
]

# 04_final_system.ipynb
nb4_cells = [
    ("markdown", "# Step 4: The Final AI Root Cause Analyzer System\nPutting it all together, this is our end-to-end RAG (Retrieval-Augmented Generation) pipeline for IT incidents."),
    ("code", "import chromadb\nimport ollama\nimport json\n\nCHROMA_PATH = \"./chroma_db\"\nCOLLECTION_NAME = \"incident_logs\"\nEMBED_MODEL = \"nomic-embed-text\"\nLLM_MODEL = \"llama3.2\"\n\nclient = chromadb.PersistentClient(path=CHROMA_PATH)\ncollection = client.get_collection(name=COLLECTION_NAME)\n\ndef get_embedding(text):\n    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)\n    return response[\"embedding\"]"),
    ("code", "def analyze_incident(system_name, error_msg):\n    print(f\"Analyzing new incident in {system_name}...\")\n    \n    # 1. Embed the new incident\n    incident_text = f\"\\nSystem: {system_name}\\nError: {error_msg}\\n\"\n    query_embedding = get_embedding(incident_text)\n    \n    # 2. Retrieve similar past incidents from ChromaDB\n    results = collection.query(\n        query_embeddings=[query_embedding],\n        n_results=2\n    )\n    \n    context = \"\\n\".join(results['documents'][0]) if results['documents'] else \"No similar historical incidents found.\"\n    \n    # 3. Generate RCA using an LLM\n    prompt = f\"\"\"\n    You are an AI IT Operations assistant.\n    \n    New Incident:\n    {incident_text}\n    \n    Historical Context (Similar past incidents):\n    {context}\n    \n    Using the historical context, please analyze the new incident.\n    Provide:\n    1. The Likely Root Cause\n    2. A Proposed Fix\n    \n    Keep it structured and concise.\n    \"\"\"\n    \n    response = ollama.chat(model=LLM_MODEL, messages=[\n        {'role': 'user', 'content': prompt}\n    ])\n    \n    return response['message']['content']"),
    ("markdown", "Let's test our complete pipeline on a brand new 500 error from the frontend!"),
    ("code", "new_system = \"frontend\"\nnew_error = \"API returned 500 Internal Server Error when clicking checkout\"\n\nfinal_report = analyze_incident(new_system, new_error)\nprint(\"\\n=== FINAL RCA REPORT ===\\n\")\nprint(final_report)")
]

if __name__ == "__main__":
    base_path = "/Users/mustakimshaikh/Downloads/ai_ analyzer /ai-root-cause-analyzer/notebooks"
    create_notebook(nb2_cells, os.path.join(base_path, "02_similarity_search.ipynb"))
    create_notebook(nb3_cells, os.path.join(base_path, "03_root_cause_llm.ipynb"))
    create_notebook(nb4_cells, os.path.join(base_path, "04_final_system.ipynb"))
    print("Notebooks generated successfully.")
