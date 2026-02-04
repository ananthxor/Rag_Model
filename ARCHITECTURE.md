# Langfuse Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         RAG Application with Langfuse                    │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐
│  User Interface │  (Flet App / CLI)
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Trace Creation                                   │
│  • User Query        → Trace: "rag_query"                               │
│  • Document Upload   → Trace: "document_upload"                         │
└────────┬────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     RAG Pipeline (Traced)                                │
│                                                                          │
│  ┌─────────────────┐         ┌─────────────────┐                       │
│  │ Vector Store    │         │ LLM Service     │                       │
│  ├─────────────────┤         ├─────────────────┤                       │
│  │ • search()      │────────▶│ • get_embedding() │                     │
│  │   [Span]        │         │   [Span]         │                      │
│  │                 │         │                  │                      │
│  │ • add_docs()    │────────▶│ • generate()     │                     │
│  │   [Span]        │         │   [Generation]   │                     │
│  └─────────────────┘         └─────────────────┘                       │
│                                                                          │
└────────┬────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      Langfuse Service                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │                     langfuse_service.py                              ││
│  │  • create_trace()      - Creates trace for user interaction         ││
│  │  • track_generation()  - Tracks LLM API calls                       ││
│  │  • track_span()        - Tracks retrieval & embeddings              ││
│  │  • flush()             - Sends events to Langfuse                   ││
│  └─────────────────────────────────────────────────────────────────────┘│
└────────┬────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Langfuse Cloud / Self-Hosted                     │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  Dashboard Features:                                                 ││
│  │  • Traces View        - Complete execution flows                    ││
│  │  • Generations View   - All LLM calls                               ││
│  │  • Analytics          - Performance metrics                         ││
│  │  • Debugging          - Inspect prompts & responses                 ││
│  └─────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Example

### Query Flow with Tracking

```
1. User asks: "What is machine learning?"
   ↓
2. Create Trace
   - trace_id: "abc123"
   - name: "rag_query"
   - metadata: {query: "What is...", model: "mistral"}
   ↓
3. Vector Retrieval (with trace_id)
   - Track Span: "vector_retrieval"
   - Input: {query: "What is...", k: 3}
   - Output: {num_results: 3, sources: ["doc1.pdf"]}
   - Time: 0.2s
   ↓
4. Embedding Generation (with trace_id)
   - Track Span: "embedding_generation"
   - Input: {text: "What is...", model: "nomic-embed-text"}
   - Output: {dimensions: 768}
   - Time: 0.1s
   ↓
5. LLM Generation (with trace_id)
   - Track Generation: "rag_streaming_generation"
   - Prompt: [system prompt + context + query]
   - Completion: "Machine learning is..."
   - Time: 2.5s
   ↓
6. Flush to Langfuse
   - All spans and generations sent
   - Available in dashboard immediately
```

## Tracked Metadata

### For Traces
- User ID
- Query text
- Model name
- Retrieval K value
- Session information

### For Generations (LLM Calls)
- Complete prompt (system + user)
- Full response
- Context length
- Response time
- Model used
- Stream vs non-stream
- Error information (if failed)

### For Spans (Retrieval & Embeddings)
- Input data
- Output data
- Processing time
- Sources retrieved
- Error information (if failed)

## Configuration

All configuration is in `.env`:

```env
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_HOST="https://cloud.langfuse.com"
LANGFUSE_ENABLED=true
```

## Benefits

✅ **Complete Visibility**: See every step of your RAG pipeline
✅ **Performance Insights**: Identify bottlenecks and optimize
✅ **Quality Tracking**: Monitor and improve response quality
✅ **Easy Debugging**: Inspect exact prompts and context used
✅ **Cost Monitoring**: Track LLM usage and costs
✅ **User Analytics**: Understand usage patterns

## Zero Overhead When Disabled

When `LANGFUSE_ENABLED=false`:
- No API calls to Langfuse
- No performance impact
- All trace_id parameters are ignored
- Application works exactly as before
