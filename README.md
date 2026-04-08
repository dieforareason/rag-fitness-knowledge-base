# Local RAG Fitness Knowledge Base

A complete local Retrieval-Augmented Generation (RAG) system for answering fitness-related questions based on PDF journals and literature.

## Architecture

This project is built using an entirely local, production-ready stack:
- **PDF Parsing & Semantic Chunking**: [Unstructured](https://unstructured.io/)
- **Embeddings Model**: `sentence-transformers` (`all-MiniLM-L6-v2`)
- **Vector Database**: [Qdrant](https://qdrant.tech/) (running locally in Docker at `localhost:6333`)
- **Local LLM Integration**: [LM Studio](https://lmstudio.ai/) running `Qwen 3.5 4B` served via an OpenAI-compatible REST API (`http://localhost:1234/v1`)

## Repository Structure

```
rag-fitness-knowledge-base/
├── data/
│   └── pdfs/              # Place your PDF documents (fitness journals/papers) here
├── ingestion.py           # Loads PDFs, performs semantic chunking, and stores them via QdrantStore
├── qdrant_store.py        # Connects to Qdrant, manages collections, and computes embeddings
├── retriever.py           # Exposes an API for executing similarity searches against Qdrant
├── llm.py                 # Connects to the local LM Studio instance to generate responses
├── app.py                 # The CLI entry point for asking questions
├── requirements.txt       # Python dependencies (to be created based on imports)
└── README.md              # Project documentation
```

## Prerequisites

1. **Python 3.8+**
2. **Docker** (Required to run Qdrant)
3. **LM Studio** (Required to run the local LLM)

## Setup & Installation

### 1. Install Dependencies

Install the necessary python dependencies using `pip`:

```bash
pip install unstructured sentence-transformers qdrant-client openai
```

*(Note: The `openai` package is strictly used as an API client to communicate locally with LM Studio. No remote OpenAI calls are made.)*

### 2. Start Qdrant Vector DB

Run a local Qdrant instance using Docker:

```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

### 3. Setup the Local LLM via LM Studio

1. Download and install **LM Studio**.
2. Within the app, search for and download the **Qwen 3.5 4B** model.
3. Navigate to the **Local Server** tab.
4. Set the Server Port to `1234` and click **Start Server**. It will be accessible at `http://localhost:1234/v1`.

## Usage

### Step 1: Data Ingestion

Place your fitness-related PDF files (papers, journals, specific topic guides like hypertrophy, volume, intensity) into the `data/pdfs/` directory. If the directory doesn't exist, simply run the script once and it will create the folder for you.

Run the ingestion script to parse, chunk semantically, and store the embeddings in Qdrant:

```bash
python ingestion.py
```

### Step 2: Query the Knowledge Base

Ask the system fitness questions via the CLI. The application will find the best chunks from your ingested PDFs and feed them to the local Qwen model to formulate a precise answer avoiding hallucinations.

```bash
python app.py "What is the optimal training volume per week for muscle hypertrophy?"
```

The app will output the retrieved context size and the final generated answer derived directly from your documents.