from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from src.config.settings import settings
import os
from typing import List
from openai import OpenAI

# Monkey-patch OpenAI client to remove unsupported parameters for Ollama
_original_create = None

def _patched_create(self, **kwargs):
    """
    Patched version of OpenAI embeddings create method.
    Removes parameters that Ollama doesn't support.
    """
    # Remove unsupported parameters
    unsupported_params = ['user', 'encoding_format', 'dimensions']
    for param in unsupported_params:
        kwargs.pop(param, None)
    
    # Call original method
    return _original_create(self, **kwargs)

def apply_openai_patch():
    """
    Apply monkey-patch to OpenAI client to make it compatible with Ollama.
    """
    global _original_create
    try:
        from openai.resources.embeddings import Embeddings
        if _original_create is None:
            _original_create = Embeddings.create
            Embeddings.create = _patched_create
            print("[OK] Applied OpenAI client patch for Ollama compatibility")
    except Exception as e:
        print(f"Warning: Could not patch OpenAI client: {e}")

# Apply the patch when this module is imported
apply_openai_patch()

class OllamaCompatibleEmbeddings(OpenAIEmbeddings):
    """
    Custom OpenAIEmbeddings that works with Ollama via LiteLLM.
    Prevents sending unsupported parameters like 'user' or 'encoding_format'.
    """
    
    def __init__(self, **kwargs):
        # Remove unsupported parameters before initialization
        kwargs.pop('dimensions', None)
        kwargs.pop('encoding_format', None)
        super().__init__(**kwargs)

def get_embeddings():
    """
    Returns the embedding function configured for LiteLLM.
    Configured to work with Ollama through LiteLLM proxy.
    """
    base_url = settings.LITELLM_BASE_URL
    
    # Use custom embeddings class that's compatible with Ollama
    return OllamaCompatibleEmbeddings(
        model=settings.EMBEDDING_MODEL,
        openai_api_base=base_url,
        openai_api_key="sk-any",  # Required by library but ignored by LiteLLM proxy
        check_embedding_ctx_length=False,
        show_progress_bar=False,
    )

def get_vector_store(session_id: str = "default"):
    """
    Returns a Chroma vector store for the specific session.
    """
    # Use session-specific collection name for isolation
    collection_name = f"{settings.COLLECTION_NAME}_{session_id}"
    
    return Chroma(
        collection_name=collection_name,
        embedding_function=get_embeddings(),
        persist_directory=settings.CHROMA_PERSIST_DIR,
    )


