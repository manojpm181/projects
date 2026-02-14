from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Optional
import math

from src.api.v1.schemas.conversations import (
    ConversationCreate, ConversationUpdate, ConversationResponse,
    ConversationListResponse, MessageCreate, MessageResponse,
    MessageListResponse, ChatRequest, ChatResponse, UsageResponse
)
from src.services.conversation_service import conversation_service
from src.services.message_service import message_service
from src.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    data: ConversationCreate,
    current_user: dict = Depends(get_current_user),
):
    """Create a new conversation."""
    
    conversation = await conversation_service.create(
        user_id=current_user["id"],
        title=data.title,
        model=data.model,
        system_prompt=data.system_prompt,
    )
    
    return conversation


@router.get("", response_model=ConversationListResponse)
async def list_conversations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    archived: bool = False,
    current_user: dict = Depends(get_current_user),
):
    """List conversations for current user."""
    
    conversations, total = await conversation_service.list_by_user(
        user_id=current_user["id"],
        page=page,
        page_size=page_size,
        archived=archived,
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    
    return ConversationListResponse(
        conversations=conversations,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Get conversation by ID."""
    
    conversation = await conversation_service.get(
        conversation_id=conversation_id,
        user_id=current_user["id"],
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return conversation


@router.patch("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: str,
    data: ConversationUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Update conversation."""
    
    updates = {k: v for k, v in data.dict().items() if v is not None}
    
    conversation = await conversation_service.update(
        conversation_id=conversation_id,
        user_id=current_user["id"],
        **updates,
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return conversation


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    soft_delete: bool = Query(True),
    current_user: dict = Depends(get_current_user),
):
    """Delete or archive conversation."""
    
    success = await conversation_service.delete(
        conversation_id=conversation_id,
        user_id=current_user["id"],
        soft_delete=soft_delete,
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )


@router.get("/{conversation_id}/messages", response_model=MessageListResponse)
async def get_messages(
    conversation_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    current_user: dict = Depends(get_current_user),
):
    """Get messages for a conversation."""
    
    messages, total = await conversation_service.get_messages(
        conversation_id=conversation_id,
        user_id=current_user["id"],
        page=page,
        page_size=page_size,
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    
    return MessageListResponse(
        messages=messages,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.post("/{conversation_id}/messages", response_model=ChatResponse)
async def send_message(
    conversation_id: str,
    data: ChatRequest,
    current_user: dict = Depends(get_current_user),
):
    """Send a message and get AI response (non-streaming)."""
    
    # Verify conversation exists
    conversation = await conversation_service.get(
        conversation_id=conversation_id,
        user_id=current_user["id"],
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    if data.stream:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use /stream endpoint for streaming"
        )
    
    try:
        # Generate response
        assistant_msg, usage = await message_service.generate_response(
            conversation_id=conversation_id,
            user_id=current_user["id"],
            user_message=data.message,
            stream=False,
        )
        
        return ChatResponse(
            message=assistant_msg,
            usage=usage,
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating response: {str(e)}"
        )