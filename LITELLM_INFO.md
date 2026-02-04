# LiteLLM Integration

We have integrated LiteLLM into your project to provide a unified API and Swagger UI for your LLMs.

## What has been done?
1. Added `litellm` and `litellm[proxy]` to `requirements.txt`.
2. Updated `start.bat` to automatically launch the LiteLLM Proxy alongside your backend server.

## How to use it?

### 1. Start the Application
Run `start.bat` as usual. You will see a new window pop up titled "LiteLLM Proxy".

### 2. Access Swagger UI
Open your browser and navigate to:
**[http://localhost:4000/](http://localhost:4000/)** (or `http://localhost:4000/docs`)

This provides an interactive Swagger UI where you can test your models defined in `llms/litellm_config.yaml`.

### 3. Current Configuration
Your `llms/litellm_config.yaml` is currently set up to proxy query to Ollama:
- **Model**: `llama-3.2-1b`
- **Upstream**: `ollama/llama3.2:1b` (running at `http://localhost:11434`)

### 4. Application Endpoints (OpenAI-Compatible)
To align with standard practices, we have added OpenAI-compatible endpoints to your **App Server (`http://localhost:8000`)**:

- **Upload File**: `POST /v1/files`
  - Accepts `file` (multipart) and optional `purpose`.
- **Chat**: `POST /v1/chat/completions`
  - Accepts standard OpenAI JSON body: `{ "messages": [...], "stream": true }`
  - Returns SSE stream compatible with OpenAI libraries.

This allows you to use standard clients to interact with your RAG app.

### 5. Integration with Backend (Optional)
Currently, your backend (`src/services/llm_service.py`) connects directly to Ollama.
If you wish to route your application traffic through LiteLLM (to leverage its logging, caching, or refusal logic), you can update `LLMService` to usage `litellm` or `openai` client pointing to `http://localhost:4000`.

Example change in `src/services/llm_service.py`:
```python
import litellm
# ...
litellm.completion(model="llama-3.2-1b", messages=...)
# or set
# os.environ["OPENAI_API_BASE"] = "http://localhost:4000"
```
