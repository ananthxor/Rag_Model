# Langfuse Integration for RAG Analytics

This document explains how to set up and use Langfuse for prompt analytics and observability in your RAG application.

## What is Langfuse?

Langfuse is an open-source observability and analytics platform for LLM applications. It helps you:
- Track all LLM requests and responses
- Monitor prompt performance
- Analyze costs and latency
- Debug and improve your RAG pipeline
- Trace complete user interactions from query to response

## Setup Instructions

### 1. Install Langfuse Package

The Langfuse package has been added to `requirements.txt`. Install it using:

```bash
pip install -r requirements.txt
```

### 2. Get Langfuse API Keys

You have two options:

#### Option A: Use Langfuse Cloud (Recommended for Quick Start)

1. Go to [https://cloud.langfuse.com](https://cloud.langfuse.com)
2. Sign up for a free account
3. Create a new project
4. Navigate to **Settings** → **API Keys**
5. Copy your **Public Key** and **Secret Key**

#### Option B: Self-Host Langfuse

Follow the [Langfuse self-hosting guide](https://langfuse.com/docs/deployment/self-host) to deploy your own instance.

### 3. Configure Environment Variables

Update your `.env` file with your Langfuse credentials:

```env
# Langfuse Configuration for Prompt Analytics
LANGFUSE_PUBLIC_KEY="pk-lf-..." # Your public key from Langfuse
LANGFUSE_SECRET_KEY="sk-lf-..." # Your secret key from Langfuse
LANGFUSE_HOST="https://cloud.langfuse.com"  # or your self-hosted URL
LANGFUSE_ENABLED=true  # Set to false to disable tracking
```

**Important:** Keep your secret key safe and never commit it to version control!

### 4. Restart Your Application

After updating the `.env` file, restart your application for the changes to take effect.

## What Gets Tracked?

The integration automatically tracks:

### 1. **User Queries**
- Complete RAG query flow from user input to final response
- Query text and metadata
- Model being used
- Retrieval parameters

### 2. **Vector Retrieval**
- Search queries to the vector database
- Number of results retrieved
- Sources retrieved
- Retrieval latency

### 3. **LLM Generations**
- All prompts sent to the LLM (both streaming and non-streaming)
- Complete responses
- Context used
- Response time
- Model information

### 4. **Embeddings**
- Text being embedded
- Embedding model used
- Processing time
- Dimensions

### 5. **Document Uploads**
- Document ingestion events
- Number of chunks created
- Processing time
- Embedding generation

## Viewing Analytics in Langfuse

### Access the Dashboard

1. Log in to [https://cloud.langfuse.com](https://cloud.langfuse.com) (or your self-hosted instance)
2. Select your project
3. You'll see various tabs:

### Traces Tab
- View complete execution traces for each user query
- See the full RAG pipeline: retrieval → context → generation
- Analyze latency at each step
- Debug failed queries

### Generations Tab
- All LLM generation events
- Compare prompts and responses
- Track streaming vs non-streaming performance
- Analyze response quality

### Analytics
- Cost tracking (if using paid LLM APIs)
- Latency metrics across different components
- Usage patterns over time
- User behavior analytics

## Example Use Cases

### 1. **Debugging Failed Queries**
If a user reports poor results, search for their query in Langfuse to see:
- What context was retrieved
- The exact prompt sent to the LLM
- The model's response
- Any errors that occurred

### 2. **Optimizing Retrieval**
Analyze retrieval metrics to:
- Determine optimal k value (number of results)
- Identify queries that return no results
- Monitor retrieval latency

### 3. **Prompt Engineering**
- Compare different versions of your system prompt
- A/B test prompt variations
- Track how changes affect response quality

### 4. **Performance Monitoring**
- Monitor response times across different components
- Identify bottlenecks in your RAG pipeline
- Track embedding generation performance

## Code Overview

### Langfuse Service (`src/services/langfuse_service.py`)
The central service that manages all Langfuse interactions:
- `create_trace()`: Creates a trace for tracking a user interaction
- `track_generation()`: Tracks LLM generation events
- `track_span()`: Tracks retrieval, embeddings, and other operations
- `flush()`: Ensures all events are sent to Langfuse

### Integration Points

1. **LLM Service** (`src/services/llm_service.py`)
   - Tracks all LLM calls (chat and embeddings)
   - Includes prompt, response, and timing data

2. **Vector Store** (`src/services/vector_store.py`)
   - Tracks retrieval operations
   - Monitors document ingestion

3. **App** (`app.py`)
   - Creates traces for user queries and document uploads
   - Orchestrates tracking across the RAG pipeline

## Disabling Langfuse

To disable Langfuse tracking without removing the code:

Set `LANGFUSE_ENABLED=false` in your `.env` file, or simply leave the API keys empty:

```env
LANGFUSE_ENABLED=false
```

The application will continue to work normally with no tracking overhead.

## Privacy & Data

- Langfuse Cloud stores your prompts and responses for analytics
- For sensitive data, consider self-hosting Langfuse
- You can configure data retention policies in Langfuse settings
- User IDs are configurable (default is "flet_user")

## Troubleshooting

### "Langfuse is enabled but API keys are missing"
- Check that your `.env` file has valid API keys
- Ensure there are no extra spaces or quotes around the keys

### No data appearing in Langfuse
- Verify `LANGFUSE_ENABLED=true` in `.env`
- Check your internet connection (for Langfuse Cloud)
- Look for error messages in the application logs
- Ensure you've restarted the application after updating `.env`

### API Key Errors
- Verify your keys are correct in the Langfuse dashboard
- Ensure you're using the correct project
- Check that your Langfuse account is active

## Advanced Configuration

### Custom User IDs
Edit the trace creation in `app.py` to use custom user IDs:

```python
trace = services.llm_service.langfuse.create_trace(
    name="rag_query",
    user_id="custom_user_id",  # Change this
    metadata={...}
)
```

### Additional Metadata
Add custom metadata to traces for better filtering:

```python
trace = services.llm_service.langfuse.create_trace(
    name="rag_query",
    user_id="flet_user",
    metadata={
        "query": query,
        "session_id": "...",
        "custom_field": "..."
    }
)
```

## Resources

- [Langfuse Documentation](https://langfuse.com/docs)
- [Langfuse Python SDK](https://langfuse.com/docs/sdk/python)
- [Langfuse GitHub](https://github.com/langfuse/langfuse)
- [Community Discord](https://discord.gg/7NXusRtqYU)

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review Langfuse documentation
3. Check application logs for error messages
4. Visit Langfuse community Discord for support
