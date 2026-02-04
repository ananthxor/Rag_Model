# Langfuse Integration Summary

This document summarizes all the changes made to integrate Langfuse for prompt analytics and API tracking.

## Overview

Langfuse has been fully integrated into the RAG application to provide:
- **Complete observability** of all LLM API requests and responses
- **Performance analytics** for retrieval, embeddings, and generation
- **Full tracing** of user interactions from query to response
- **Debugging capabilities** to inspect prompts, context, and responses

## Files Modified

### 1. **requirements.txt**
- Added `langfuse` package dependency

### 2. **.env**
- Added Langfuse configuration variables:
  - `LANGFUSE_PUBLIC_KEY` - Your Langfuse public API key
  - `LANGFUSE_SECRET_KEY` - Your Langfuse secret API key
  - `LANGFUSE_HOST` - Langfuse server URL (cloud or self-hosted)
  - `LANGFUSE_ENABLED` - Toggle to enable/disable tracking

### 3. **src/config/settings.py**
- Added Langfuse settings to the Settings class:
  - `LANGFUSE_PUBLIC_KEY: str`
  - `LANGFUSE_SECRET_KEY: str`
  - `LANGFUSE_HOST: str`
  - `LANGFUSE_ENABLED: bool`

### 4. **src/services/llm_service.py**
- Added trace_id parameter to all methods
- Integrated Langfuse tracking for:
  - `generate_response()` - Tracks non-streaming LLM calls
  - `generate_response_stream()` - Tracks streaming LLM calls
  - `get_embedding()` - Tracks embedding generation
- Tracks metadata including:
  - Question and context length
  - Response time
  - Model information
  - Error tracking

### 5. **src/services/vector_store.py**
- Added trace_id parameter to tracking methods
- Integrated Langfuse tracking for:
  - `add_documents()` - Tracks document ingestion and embedding
  - `search()` - Tracks vector retrieval operations
- Tracks metadata including:
  - Number of chunks/results
  - Processing time
  - Sources retrieved

### 6. **app.py**
- Added trace creation for user queries
- Added trace creation for document uploads
- Integrated trace_id propagation through the RAG pipeline
- Added Langfuse flush calls to ensure events are sent

## Files Created

### 1. **src/services/langfuse_service.py**
A dedicated service to manage all Langfuse interactions:
- `LangfuseService` class with methods:
  - `create_trace()` - Creates a new trace for user interactions
  - `track_generation()` - Tracks LLM generation events
  - `track_span()` - Tracks retrieval, embeddings, and other operations
  - `flush()` - Sends pending events to Langfuse
- Singleton instance `langfuse_service` for easy access
- Automatic error handling and logging

### 2. **LANGFUSE_SETUP.md**
Comprehensive documentation covering:
- What Langfuse is and why it's useful
- Setup instructions (Cloud and self-hosted)
- Configuration guide
- What gets tracked
- How to view analytics in the dashboard
- Use cases and examples
- Troubleshooting guide
- Privacy considerations

### 3. **example_langfuse.py**
Demonstration script showing:
- How to check Langfuse configuration
- Creating traces
- Tracking embeddings
- Tracking LLM generations
- Tracking streaming responses
- Complete working examples

### 4. **README.md** (Updated)
- Added Langfuse setup step
- Added Features section highlighting Langfuse capabilities
- Reference to LANGFUSE_SETUP.md and example_langfuse.py

## What Gets Tracked

### User Query Flow
```
User Query
    ↓
[Trace Created: "rag_query"]
    ↓
Vector Retrieval
    ↓
[Span: "vector_retrieval"]
    ├─ Query text
    ├─ Number of results
    ├─ Sources found
    └─ Retrieval time
    ↓
Embedding Generation (for query)
    ↓
[Span: "embedding_generation"]
    ├─ Text to embed
    ├─ Model used
    ├─ Embedding dimensions
    └─ Processing time
    ↓
LLM Generation
    ↓
[Generation: "rag_streaming_generation"]
    ├─ Full prompt (system + user)
    ├─ Context provided
    ├─ Complete response
    ├─ Response time
    ├─ Model used
    └─ Response length
```

### Document Upload Flow
```
Document Upload
    ↓
[Trace Created: "document_upload"]
    ↓
Document Processing
    ↓
Embedding Generation (for chunks)
    ↓
[Span: "document_ingestion"]
    ├─ Number of chunks
    ├─ Source files
    ├─ Embeddings created
    └─ Processing time
```

## Benefits

1. **Debugging**: See exactly what context was used for each query
2. **Optimization**: Identify slow operations in your RAG pipeline
3. **Quality**: Track and improve response quality over time
4. **Analytics**: Understand usage patterns and user behavior
5. **Cost Tracking**: Monitor LLM usage and costs (if using paid APIs)

## Usage

### Enable Tracking
1. Get API keys from [cloud.langfuse.com](https://cloud.langfuse.com)
2. Update `.env` with your keys
3. Set `LANGFUSE_ENABLED=true`
4. Restart the application

### View Analytics
1. Log in to Langfuse dashboard
2. Navigate to your project
3. Explore:
   - **Traces**: Complete user interaction flows
   - **Generations**: All LLM calls
   - **Analytics**: Performance metrics and insights

### Run Example
```bash
python example_langfuse.py
```

### Disable Tracking
Set `LANGFUSE_ENABLED=false` in `.env` or leave API keys empty.

## Implementation Notes

- **Non-intrusive**: All tracking is optional and can be disabled
- **Zero overhead when disabled**: No performance impact if LANGFUSE_ENABLED=false
- **Backward compatible**: Existing code continues to work
- **Error handling**: Tracking failures don't affect application functionality
- **Async-safe**: Works with both sync and streaming responses

## Next Steps

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Configure Langfuse**: Follow [LANGFUSE_SETUP.md](LANGFUSE_SETUP.md)
3. **Run example**: `python example_langfuse.py`
4. **Monitor your RAG pipeline**: Start using the application and view analytics in Langfuse

## Support

For detailed setup instructions and troubleshooting, see [LANGFUSE_SETUP.md](LANGFUSE_SETUP.md).
