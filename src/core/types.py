from pydantic import BaseModel
from typing import List, Optional, Union, Dict, Any

# --- Original Application Types ---
class DocumentChunk(BaseModel):
    content: str
    source_id: str
    metadata: Dict[str, Any]

class SearchResult(BaseModel):
    content: str
    score: float
    source: str

class RagResponse(BaseModel):
    """Standard response format."""
    answer: str
    sources: List[str]
    context_used: str

# --- OpenAI/LiteLLM Compatible Types ---
class ChatMessage(BaseModel):
    role: str
    content: str
    name: Optional[str] = None
    function_call: Optional[Dict[str, Any]] = None

class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "default"
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1
    stream: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None

class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Optional[str] = "stop"

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Optional[Dict[str, int]] = None
