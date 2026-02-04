✅ RAG Training = NOT training the LLM

In RAG, the LLM remains frozen.
You don’t fine-tune it.

The “training” happens on your data, not the model.

RAG training includes:

✔ 1. Chunking your documents properly
✔ 2. Creating embeddings from those chunks
✔ 3. Building a vector database
✔ 4. Adding metadata / titles
✔ 5. Setting up retrieval logic

None of these steps modify Llama 3.2–1B.
1. Embedding Model Fine-tuning (not Llama fine-tuning)

Example: fine-tune BERT/Sentence-Transformers embeddings so that retrieval improves.

2. Rerankers Training

Teach the system which search results are better.

3. Query Rewriting Models

Improve user queries before retrieval.

4. Prompt Tuning

You tune prompts and system instructions.

❌ Training the main LLM is NOT useful for RAG

Most RAG systems keep the base LLM untouched because:

fine-tuned LLMs hallucinate more

RAG accuracy drops

cost/time increases

you lose general abilities of the model

User Query
     ↓
Query Rewriter (optional)
     ↓
Embed Query
     ↓
Vector DB Search
     ↓
Rerank Results (optional)
     ↓
Retrieved Chunks
     ↓
LLM (Llama 3.2-1B) Answers using those chunks
