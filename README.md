# Local RAG System 🧠

A powerful, locally-hosted Retrieval-Augmented Generation (RAG) system built for privacy, speed, and observability. This project leverages **Ollama** for local LLM inference, **ChromaDB** for vector storage, and **FastAPI** for the backend, with multiple client interfaces (Flet & Flutter) and **Langfuse** for robust tracing and analytics.

---

## 🏗️ Architecture

The system operates in two main phases: **Ingestion** (Learning) and **Inference** (Thinking).

### 1. Ingestion Pipeline
1.  **Document Loading**: PDF processing using `PyMuPDF` (Fitz).
2.  **Chunking**: Splitting text into manageable chunks (default: 300 words).
3.  **Embedding**: Converting text to vectors using `nomic-embed-text` via Ollama.
4.  **Storage**: Indexing vectors and metadata in **ChromaDB**.

### 2. Inference Pipeline (RAG)
1.  **Query Embedding**: Converting user question to vector.
2.  **Retrieval**: Performing Cosine Similarity search in ChromaDB to find top-k relevant context.
3.  **Reranking/Processing**: Constructing an augmented prompt with retrieved context.
4.  **Generation**: Generates response using `llama3.2:1b` (or configured model) via **LiteLLM**.

### 3. Observability & Routing
*   **Langfuse**: Full-stack tracing of queries, retrievals, and generations.
*   **LiteLLM**: Unified interface for LLM calls, handling routing and fallback.

---

## 🚀 Tech Stack

*   **Logic Core**: Python 3.10+, LangChain, LiteLLM
*   **Vector Database**: ChromaDB
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
    *   Create a `.env` file (copy from example if available, or set up fresh).
    *   **Langfuse (Optional but Recommended)**:
        ```env
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

### 4. Mobile App (Flutter)
Native Android/iOS experience:
```bash
cd flutter_client
# ... setup flutter project ...
flutter run
```
*(Requires FastAPI server running on tailored IP/localhost)*

---

## 🔍 Features

*   **Privacy First**: Runs entirely locally (unless using cloud observability).
*   **Multi-Modal Ready**: Architecture supports expanding to vision models.
*   **Production Grade**: 
    *   **Tracing**: Debug complex queries with Langfuse.
    *   **Async**: Non-blocking ingestion and inference.
    *   **Scalable**: Modular service architecture (`src/services`).

## 📂 Project Structure

*   `src/`: Core source code.
    *   `services/`: Business logic (LLM, Vector Store, Ingestion).
    *   `core/`: Type definitions and configurations.
    *   `server.py`: FastAPI application.
*   `flutter_client/`: Native mobile application code.
*   `app.py`: Flet client entry point.
*   `main.py`: CLI entry point.
