# Why "LiteLLM" is listed as the Provider

You noticed that your Langfuse logs show `"provider": "litellm"`.
This is **correct** and completely expected.

## 1. Why does it say LiteLLM?
In your code (`src/services/llm_service.py`), we explicitly tell Langfuse to label it this way:

```python
self.langfuse.track_span(
    ...
    metadata={
        "provider": "litellm"  <-- HERE
    }
)
```

We do this because LiteLLM is the **standardized interface** we are using. Under the hood, LiteLLM forwards the request to **Ollama** running locally on your machine.

## 2. How is LiteLLM helping?
LiteLLM is acting as a **Universal Adapter**.

*   **without LiteLLM**: You would have to write custom code for Ollama (`requests.post('http://localhost:11434/api/generate')`). If you ever wanted to switch to OpenAI or Anthropic later, you would have to rewrite your entire backend.
*   **with LiteLLM**: You write code ONCE using the standard OpenAI format. LiteLLM translates it for whatever model you are using (Ollama, GPT-4, Claude, etc.).

### Visual Diagram
```mermaid
graph LR
    A[Your App] -->|OpenAI Format| B[LiteLLM Proxy]
    B -->|Translation| C[Ollama (Local)]
    B -->|Logging| D[Langfuse]
```

## 3. Summary
*   **Provider**: LiteLLM (The adapter you are talking to)
*   **Real Model**: Ollama / Llama-3.2 (The brain doing the work)
*   **Benefit**: Future-proof code and easy logging.
