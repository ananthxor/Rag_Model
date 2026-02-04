# How LocalRAG Works 🧠

This document explains exactly what happens under the hood when you Upload a file and when you Ask a question.

---

## Phase 1: Uploading & Ingestion (The "Learning" Phase) 📥

When you upload a PDF (e.g., `Health.pdf`), the system does not just "save" it. It "reads and memorizes" it.

### Step 1: Text Extraction 📄
*   **Action**: The file is passed to `DocumentProcessor`.
*   **Tool**: We use **PyMuPDF (Fitz)** to open the PDF.
*   **Process**: It iterates through every page (1 to 86) and extracts the raw text. 
    *   *Note: Since we disabled Vision, it strictly reads the text layer. If the text layer is corrupted (garbled symbols), it reads garbage.*

### Step 2: Chunking ✂️
*   **Action**: The massive block of text is chopped into small pieces called **Chunks**.
*   **Why?**: AI models have a memory limit. They can't read 86 pages at once.
*   **Config**: `CHUNK_SIZE=300` words.
*   **Result**: Your PDF becomes ~100 separate small notes.

### Step 3: Vectorization (Embedding) 🔢
*   **Action**: Every chunk is sent to the **Embedding Model** (`nomic-embed-text`).
*   **Magic**: The model converts the text into a list of 768 numbers (a "Vector").
    *   *Example*: "Aerobics is good" → `[0.12, -0.98, 0.45, ...]`
*   **Purpose**: Computers understand numbers, not words. Similar concepts get similar numbers.

### Step 4: Storage 💾
*   **Action**: The vectors + original text are saved into **ChromaDB** (our Vector Database).
*   **Location**: Transient memory (RAM) or disk depending on setup.

---

## Phase 2: Asking & Answering (The "Thinking" Phase) 💬

When you ask: *"What are the benefits of Aerobics?"*

### Step 1: Query Embedding 🔢
*   **Action**: Your question is sent to the same Embedding Model (`nomic-embed-text`).
*   **Result**: It becomes a vector: `[0.14, -0.99, 0.42, ...]`.

### Step 2: Similarity Search (Retrieval) 🔍
*   **Action**: We compare your Question Vector vs. all 100 Document Vectors in the database.
*   **Math**: We calculate "Cosine Similarity" (how close the angles of the vectors are).
*   **Result**: We pick the **Top 3** chunks (`Retrieval_K=3`) that are mathematically closest to your question.
    *   *Example*: It finds Page 12, Page 45, and Page 46.

### Step 3: Prompt Construction 📝
*   **Action**: The system builds a "Prompt" for the LLM. It looks like this:
    ```text
    SYSTEM: You are a helpful assistant.
    USER: 
    CONTEXT:
    (Content of Page 12...)
    (Content of Page 45...)
    (Content of Page 46...)

    QUESTION: What are the benefits of Aerobics?
    ```

### Step 4: Generation (The Laggy Part) 🐢
*   **Action**: This huge block of text is sent to **Llama 3.2:1b** (the LLM).
*   **Process**: 
    1.  The LLM "reads" the context (Processing).
    2.  It uses its training to "understand" the relationship between the context and the question.
    3.  It **generates** the answer token-by-token (Typing).
*   **Output**: "Aerobics improves cardiovascular health..."

---

## Summary of Latency ⏱️

*   **Ingestion Time**: Depends on PDF size. (Text extraction is fast; Embeddings take ~0.1s per chunk).
*   **Query Time**:
    *   **Retrieval**: Very fast (< 0.2s).
    *   **Generation**: Slow (2s - 10s). This depends on your GPU/CPU speed.
