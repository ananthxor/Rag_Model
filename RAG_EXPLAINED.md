# Why does it take time? (RAG Architecture Explained)

You asked: *"We have made the data to vectors, so why does it take time again when a user asks a question?"*

This is a great question. It takes time because **Vectorization (Indexing)** is only half the battle. The other half is **Generation (Reading & Writing)**, which happens in real-time.

Here is the breakdown of time spent on a query:

### 1. The Pre-Work (What we already did) ✅
*   **Ingestion**: We converted your PDF into vectors.
*   **Result**: The "Library" is built. This part is done.

### 2. The User Request (What happens when you ask) ⏳
When you ask *"What does the sign say?"*, the system performs these 4 steps live:

1.  **Embedding Query (Fast - 0.1s)**:
    *   It converts your *question* into a vector (numbers) so it matches the library format.
    *   *Why again?* Because we didn't know your question beforehand.

2.  **Retrieval Search (Fast - 0.1s)**:
    *   It scans the library to find the most relevant pages (e.g., Page 5 and 6).
    *   *Result*: It finds the raw text/descriptions.

3.  **Constructing Prompt (Instant)**:
    *   It pastes the found text into a prompt for the AI:
        > "Here is some context from the user's document: [Content of Page 5...]. Based on this, answer the question: What does the sign say?"

4.  **LLM Generation (SLOW - 2s to 10s)**: 🐢🐢🐢
    *   **This is the bottleneck.**
    *   The AI (Llama 3.2 1B or Mistral) typically reads the context and **writes the answer word-by-word**.
    *   It is "thinking" and "typing" in real-time. It cannot pre-calculate this because the answer depends entirely on your specific question.

---

## ⚡ How to speed it up?

We can optimize the trade-off between **Speed** vs **Intelligence**.

### Option A: Use a Faster Model (Current)
*   **Model**: `llama3.2:1b`
*   **Speed**: Very Fast.
*   **Quality**: Good for simple questions.

### Option B: Retrieve Less Context
*   Currently, we read **5 pages** (`Retrieval_K=5`).
*   The AI has to read all 5 pages before answering.
*   **Fix**: Lower it to **3 pages**. This reduces reading time.

### Option C: Avoid Model Swapping (Hardware Limitation)
*   **Problem**: If you use `llava` for Vision (images) and `llama3.2` for Chat.
*   **Latency**: Your computer has to **unload** Llava from RAM and **load** Llama 3.2. This takes 5-10 seconds.
*   **Fix**: Once you start chatting, if you stick to text questions, it stays fast after the first swap.

## 🛠 Recommended Fix

I have already optimized the system to be as fast as possible. If you want it faster, you can lower the retrieval count in `src/config/settings.py`:

```python
Retrieval_K: int = 3  # Change from 5 to 3
```
