from typing import List, Dict, Optional, AsyncGenerator
import uuid
import time

from src.core.supabase import supabase_admin
from src.services.llm_service import llm_service
from src.llm.token_counter import token_counter
from src.llm.prompts import Prompts
from src.services.conversation_service import conversation_service


class MessageService:
    """Message management and LLM interaction service."""
    
    @staticmethod
    async def create(
        conversation_id: str,
        role: str,
        content: str,
        model: Optional[str] = None,
        token_count: Optional[int] = None,
        finish_reason: Optional[str] = None,
        latency_ms: Optional[int] = None,
    ) -> Dict:
        """Create a new message."""
        
        if token_count is None:
            token_count = await llm_service.count_tokens(content)
        
        message = {
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
            "token_count": token_count,
            "model": model,
            "finish_reason": finish_reason,
            "latency_ms": latency_ms,
        }
        
        response = supabase_admin.table("messages")\
            .insert(message)\
            .execute()
        
        return response.data[0] if response.data else None
    
    @staticmethod
    async def get_conversation_messages(
        conversation_id: str,
        user_id: str,
        include_system: bool = True,
    ) -> List[Dict]:
        """Get all messages for conversation formatted for LLM."""
        
        # Get conversation
        conversation = await conversation_service.get(conversation_id, user_id)
        if not conversation:
            return []
        
        # Get messages
        response = supabase_admin.table("messages")\
            .select("*")\
            .eq("conversation_id", conversation_id)\
            .order("created_at")\
            .execute()
        
        messages = response.data or []
        
        # Format for LLM
        formatted = []
        
        # Add system prompt if available
        if include_system and conversation.get("system_prompt"):
            formatted.append({
                "role": "system",
                "content": conversation["system_prompt"]
            })
        
        # Add user and assistant messages
        for msg in messages:
            formatted.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Truncate if too long
        formatted = token_counter.truncate_messages(formatted)
        
        return formatted
    
    @staticmethod
    async def generate_response(
        conversation_id: str,
        user_id: str,
        user_message: str,
        stream: bool = False,
    ) -> Dict | AsyncGenerator:
        """Generate AI response using Groq free tier."""
        
        start_time = time.time()
        
        # Save user message
        user_msg = await MessageService.create(
            conversation_id=conversation_id,
            role="user",
            content=user_message,
        )
        
        # Get conversation
        conversation = await conversation_service.get(conversation_id, user_id)
        
        # Get formatted messages for LLM
        messages = await MessageService.get_conversation_messages(
            conversation_id, user_id
        )
        
        try:
            if stream:
                # Streaming response
                stream_gen = await llm_service.generate_response(
                    messages=messages,
                    stream=True,
                    model=conversation["model"],
                )
                
                return stream_gen, conversation
            
            # Non-streaming response
            response = await llm_service.generate_response(
                messages=messages,
                stream=False,
                model=conversation["model"],
            )
            
            # Save assistant message
            assistant_msg = await MessageService.create(
                conversation_id=conversation_id,
                role="assistant",
                content=response["content"],
                model=response["model"],
                token_count=response["output_tokens"],
                finish_reason=response["finish_reason"],
                latency_ms=response["latency_ms"],
            )
            
            # Generate title if this is first message
            messages_count = len(messages)
            if messages_count <= 2:  # First exchange
                title = Prompts.generate_title(user_message)
                await conversation_service.update(
                    conversation_id,
                    user_id,
                    title=title
                )
            
            return assistant_msg, response
            
        except Exception as e:
            # Save error message
            await MessageService.create(
                conversation_id=conversation_id,
                role="assistant",
                content=f"Error: {str(e)}",
                finish_reason="error",
            )
            raise e


message_service = MessageService()