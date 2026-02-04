from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.rag.vector_store import get_vector_store
from src.config.settings import settings
import os
import shutil

def ingest_file(file_path: str, session_id: str):
    """
    Ingests a file into the vector store for a given session.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    # 1. Load Documents
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
        
    docs = loader.load()
    
    # 2. Split Documents
    # Use config chunk size (which was 300 words). Convert approx to chars (x4) or use explicit setting
    # Let's assume settings.CHUNK_SIZE is words, but usually recursively uses chars.
    # 300 words ~ 1200-1500 chars.
    chunk_size = settings.CHUNK_SIZE * 4 
    chunk_overlap = settings.CHUNK_OVERLAP * 4
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = splitter.split_documents(docs)
    
    # 3. Add Metadata
    filename = os.path.basename(file_path)
    for chunk in chunks:
        chunk.metadata["session_id"] = session_id
        chunk.metadata["source"] = filename # Simplify source to just filename for display
        # We might need the unique ID in metadata for deletion
        chunk.metadata["file_id"] = f"{session_id}_{filename}"

    # 4. Index
    vector_store = get_vector_store(session_id)
    vector_store.add_documents(chunks)
    
    return len(chunks)

def delete_document(filename: str, session_id: str):
    """
    Deletes a document from the vector store.
    """
    vector_store = get_vector_store(session_id)
    
    # Chroma doesn't support delete by metadata efficiently in all versions, 
    # but LangChain wrapper exposes .delete(ids=[...])
    # or we can use get() to find IDs first.
    
    # We need to find IDs where source == filename
    # Note: Depending on how we stored it. 
    
    # In LangChain params:
    # vector_store.delete(ids=[...])
    
    # We retrieve first
    results = vector_store.get(where={"source": filename})
    if results and results['ids']:
        vector_store.delete(ids=results['ids'])
        return True
    return False

def clear_session_data(session_id: str):
    """
    Clears the entire collection for the session.
    """
    vector_store = get_vector_store(session_id)
    vector_store.delete_collection()
