from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ConversationCreate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    model: Optional[str] = "llama3-8b-8192"
    system_prompt: Optional[str] = None


class ConversationUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    system_prompt: Optional[str] = None
    is_archived: Optional[bool] = None


class ConversationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    model: str
    system_prompt: Optional[str] = None
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ConversationListResponse(BaseModel):
    conversations: List[ConversationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class MessageCreate(BaseModel):
    content: str


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    token_count: int = 0
    model: Optional[str] = None
    finish_reason: Optional[str] = None
    latency_ms: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageListResponse(BaseModel):
    messages: List[MessageResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ChatRequest(BaseModel):
    message: str
    stream: bool = False


class ChatResponse(BaseModel):
    message: MessageResponse
    usage: Dict[str, Any]


class UsageResponse(BaseModel):
    total_tokens: int
    total_messages: int
    total_conversations: int
    model_usage: Dict[str, int]