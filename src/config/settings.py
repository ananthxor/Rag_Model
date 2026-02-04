from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "LocalRAG"
    VERSION: str = "1.0.0"
    
    # Vector DB Settings
    CHROMA_PERSIST_DIR: str = "./rag_db"
    COLLECTION_NAME: str = "user_docs"
    
    # Model Settings
    LLM_MODEL: str = "llama-3.2-1b" # LiteLLM Alias
    VISION_MODEL: str = "llava" # For analyzing images in docs
    EMBEDDING_MODEL: str = "nomic-embed-text"
    
    
    # Retrieval Settings
    Retrieval_K: int = 5  # Number of docs to retrieve (Higher = Better Recall)
    
    # Processing Settings
    CHUNK_SIZE: int = 300
    CHUNK_OVERLAP: int = 30

    # Langfuse Settings for Prompt Analytics
    LANGFUSE_SECRET_KEY: str = "sk-lf-79573c9a-e98b-416f-ae54-6d84e1c90a09"
    LANGFUSE_PUBLIC_KEY: str = "pk-lf-3b16fa78-c1c7-448b-b5ed-4af4fdc158aa"
    LANGFUSE_BASE_URL: str = "http://127.0.0.1:3000"
    LANGFUSE_ENABLED: bool = True
    
    # LiteLLM Settings
    LITELLM_BASE_URL: str = "http://127.0.0.1:4000"

    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
# Force reload for .env update
