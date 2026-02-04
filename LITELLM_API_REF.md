# LiteLLM Proxy API Reference

The LiteLLM Proxy (running on Port 4000) provides a **OpenAI-compatible** interface to your underlying models (like Ollama). This means you can use any OpenAI client library to interact with it.

Below are the key API endpoints available:

## 1. Chat Completions
**Endpoint**: `POST /chat/completions`

This is the primary endpoint for generating text and chat responses.

**Request Body**:
```json
{
  "model": "llama-3.2-1b", 
  "messages": [
    { "role": "system", "content": "You are a helpful assistant." },
    { "role": "user", "content": "Hello!" }
  ],
  "temperature": 0.7,
  "max_tokens": 100,
  "stream": false
}
```

**Response**:
```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "llama-3.2-1b",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Hello there! How can I help you today?"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}
```

## 2. List Models
**Endpoint**: `GET /models`

Returns a list of all models currently configured and available via the proxy.

**Response**:
```json
{
  "data": [
    {
      "id": "llama-3.2-1b",
      "object": "model",
      "created": 1677610602,
      "owned_by": "openai" 
    }
  ],
  "object": "list"
}
```

## 3. Completions (Legacy)
**Endpoint**: `POST /completions`

Legacy endpoint for raw text completion (non-chat). Prefer `/chat/completions` for most modern models.

## 4. Embeddings (Optional)
**Endpoint**: `POST /embeddings`

Generates vector embeddings for a given text input. (Requires embedding model to be configured in `litellm_config.yaml`)

**Request Body**:
```json
{
  "model": "nomic-embed-text",
  "input": "The quick brown fox jumps over the lazy dog"
}
```

## How to use with Python

You can use the official `openai` python package:

```python
import openai

client = openai.OpenAI(
    api_key="anything",       # LiteLLM needs a key, but for local it can be anything
    base_url="http://localhost:4000"
)

response = client.chat.completions.create(
    model="llama-3.2-1b",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```
