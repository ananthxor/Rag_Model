# Local RAG System 🧠

A powerful, locally-hosted Retrieval-Augmented Generation (RAG) system built for privacy, speed, and observability. This project leverages **Ollama** for local LLM inference, **ChromaDB** for vector storage, and **FastAPI** for the backend, with multiple client interfaces (Flet & Flutter) and **Langfuse** for robust tracing and analytics.

---

## 🏗️ Architecture

The system operates in two main phases: **Ingestion** (Learning) and **Inference** (Thinking).

### 1. Ingestion Pipeline
1.  **Document Loading**: PDF processing using `PyMuPDF` (Fitz).
2.  **Advanced Chunking** (New):
    *   **Recursive**: Intelligent splitting on paragraphs/sentences.
    *   **Sentence-based**: Linguistically aware splitting using spaCy.
    *   **Configurable Overlap**: Preserves context across chunks.
3.  **Embedding**: Converting text to vectors using `nomic-embed-text` via Ollama.
4.  **Storage**: Indexing vectors in **ChromaDB** and keywords in **BM25 Index**.

### 2. Inference Pipeline (RAG)
1.  **Query Embedding**: Converting user question to vector.
2.  **Hybrid Retrieval** (New):
    *   **Semantic Search**: Vector similarity (Cosine/L2).
    *   **Keyword Search**: BM25 algorithm for exact term matching.
    *   **Fusion**: Weighted combination of scores (e.g., 70% Semantic + 30% Keyword).
3.  **Processing**: Constructing an augmented prompt with retrieved context.
4.  **Generation**: Generates response using `llama3.2:1b` (or configured model) via **LiteLLM**.

### 3. Observability & Routing
*   **Langfuse**: Full-stack tracing of queries, retrievals, scores, and generations.
*   **LiteLLM**: Unified interface for LLM calls, handling routing and fallback.

---

## 🚀 Tech Stack

*   **Logic Core**: Python 3.10+, LangChain, LiteLLM
*   **Vector Database**: ChromaDB
*   **Retrieval Engine**: Hybrid (Vector + BM25)
*   **LLM Runtime**: Ollama (Llama 3.2, Nomic Embed)
*   **API**: FastAPI, Uvicorn
*   **Frontend**: 
    *   **Desktop/Web**: Flet (Python)
    *   **Mobile**: Flutter (Dart)
*   **Observability**: Langfuse (Self-hosted or Cloud)

---

## 🛠️ Prerequisites

1.  **Ollama**: Install from [ollama.com](https://ollama.com/).
2.  **Models**: Pull the required models:
    ```bash
    ollama pull llama3.2:1b
    ollama pull nomic-embed-text
    ```
3.  **Python**: Ensure Python 3.10 or higher is installed.
4.  **Text Processing**:
    ```bash
    python -m spacy download en_core_web_sm
    ```

---

## 📦 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/ananthxorstack/Rag_Model.git
    cd Rag_Model
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configuration**
    *   Create a `.env` file with new settings:
    ```env
    # RAG Settings
    CHUNK_SIZE=500
    CHUNK_OVERLAP=100
    CHUNK_STRATEGY=recursive    # recursive, sentence
    
    # Hybrid Search
    HYBRID_SEARCH_ENABLED=true
    HYBRID_SEMANTIC_WEIGHT=0.7
    HYBRID_BM25_WEIGHT=0.3

    # Langfuse (Optional)
    LANGFUSE_SECRET_KEY=sk-lf-...
    LANGFUSE_PUBLIC_KEY=pk-lf-...
    LANGFUSE_HOST=https://cloud.langfuse.com
    LANGFUSE_ENABLED=true
    ```

---

## 💻 Usage

### 1. API Server (Backend)
Start the high-performance FastAPI server:
```bash
uvicorn src.server:app --reload
```
*   **Swagger Docs**: `http://127.0.0.1:8000/docs`
*   **Endpoints**: `/ingest/`, `/ask/`, `/chat/`

### 2. Desktop/Web App (Flet)
Launch the cross-platform UI:
```bash
flet run app.py
```
*   Use `--web` to run in browser.

### 3. Command Line Interface (CLI)
Quick interactions via terminal:
```bash
# Ingest a document
python main.py ingest "docs/manual.pdf"

# Ask a question
python main.py ask "How do I reset the device?"
```

---

## 🔍 Features

*   **Privacy First**: Runs entirely locally (unless using cloud observability).
*   **Hybrid Search**: Combines vector semantic search with BM25 keyword matching for superior accuracy.
*   **Advanced Chunking**: Uses linguistic analysis (spaCy) to split text without breaking sentences.
*   **Production Grade**: 
    *   **Tracing**: Debug complex queries with Langfuse.
    *   **Async**: Non-blocking ingestion and inference.
    *   **Scalable**: Modular service architecture (`src/services`).

## 📂 Project Structure

*   `src/`: Core source code.
    *   `services/`: Business logic.
        *   `chunking_service.py`: Intelligent text splitting.
        *   `hybrid_search.py`: BM25 + Vector retrieval.
        *   `vector_store.py`: ChromaDB integration.
        *   `llm_service.py`: LiteLLM wrapper.
    *   `core/`: Type definitions and configurations.
    *   `server.py`: FastAPI application.
*   `flutter_client/`: Native mobile application code.
*   `app.py`: Flet client entry point.
*   `main.py`: CLI entry point.
