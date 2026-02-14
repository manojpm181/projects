from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.responses import StreamingResponse
import json
import asyncio

from src.api.v1.schemas.conversations import ChatRequest
from src.services.message_service import message_service
from src.services.conversation_service import conversation_service
from src.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/streaming", tags=["streaming"])


@router.post("/conversations/{conversation_id}/stream")
async def stream_message(
    conversation_id: str,
    data: ChatRequest,
    request: Request,
    current_user: dict = Depends(get_current_user),
):
    """Stream AI response using Server-Sent Events (FREE)."""
    
    # Verify conversation
    conversation = await conversation_service.get(
        conversation_id=conversation_id,
        user_id=current_user["id"],
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    if not data.stream:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stream parameter must be true"
        )
    
    async def event_generator():
        """Generate SSE events."""
        
        collected_content = []
        message_id = None
        
        try:
            # Get streaming generator
            stream_gen, _ = await message_service.generate_response(
                conversation_id=conversation_id,
                user_id=current_user["id"],
                user_message=data.message,
                stream=True,
            )
            
            # Stream each chunk
            async for chunk in stream_gen:
                if chunk["type"] == "delta":
                    collected_content.append(chunk["content"])
                    
                    # Send delta event
                    yield f"event: delta\ndata: {json.dumps({'content': chunk['content']})}\n\n"
                
                elif chunk["type"] == "complete":
                    # Send complete event
                    yield f"event: complete\ndata: {json.dumps({
                        'content': chunk['content'],
                        'finish_reason': chunk['finish_reason'],
                        'tokens': chunk['output_tokens'],
                        'latency_ms': chunk['latency_ms'],
                    })}\n\n"
                    
                    # Save message
                    assistant_msg = await message_service.create(
                        conversation_id=conversation_id,
                        role="assistant",
                        content=chunk['content'],
                        model=conversation["model"],
                        token_count=chunk['output_tokens'],
                        finish_reason=chunk['finish_reason'],
                        latency_ms=chunk['latency_ms'],
                    )
                    
                    message_id = str(assistant_msg["id"])
                
                elif chunk["type"] == "error":
                    # Send error event
                    yield f"event: error\ndata: {json.dumps({'error': chunk['error']})}\n\n"
                
                # Check if client disconnected
                if await request.is_disconnected():
                    break
                
                # Small delay to prevent overwhelming
                await asyncio.sleep(0.01)
            
            # Send done event
            if message_id:
                yield f"event: done\ndata: {json.dumps({'message_id': message_id})}\n\n"
            
        except Exception as e:
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


@router.get("/health")
async def stream_health():
    """Check streaming endpoint health."""
    return {"status": "ok", "service": "streaming"}