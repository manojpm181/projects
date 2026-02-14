from typing import List, Dict, Optional, Tuple
import uuid
from datetime import datetime

from src.core.supabase import supabase_admin
from src.llm.prompts import Prompts
from src.core.config import settings


class ConversationService:
    """Conversation management service."""
    
    @staticmethod
    async def create(
        user_id: str,
        title: Optional[str] = None,
        model: str = settings.DEFAULT_MODEL,
        system_prompt: Optional[str] = None,
    ) -> Dict:
        """Create a new conversation."""
        
        conversation = {
            "user_id": user_id,
            "title": title or "New Conversation",
            "model": model,
            "system_prompt": system_prompt or Prompts.DEFAULT,
            "is_archived": False,
        }
        
        response = supabase_admin.table("conversations")\
            .insert(conversation)\
            .execute()
        
        return response.data[0] if response.data else None
    
    @staticmethod
    async def get(conversation_id: str, user_id: str) -> Optional[Dict]:
        """Get conversation by ID."""
        
        response = supabase_admin.table("conversations")\
            .select("*")\
            .eq("id", conversation_id)\
            .eq("user_id", user_id)\
            .execute()
        
        return response.data[0] if response.data else None
    
    @staticmethod
    async def list_by_user(
        user_id: str,
        page: int = 1,
        page_size: int = 20,
        archived: bool = False,
    ) -> Tuple[List[Dict], int]:
        """List conversations for user."""
        
        offset = (page - 1) * page_size
        
        # Get total count
        count_response = supabase_admin.table("conversations")\
            .select("*", count="exact")\
            .eq("user_id", user_id)\
            .eq("is_archived", archived)\
            .execute()
        
        total = count_response.count if hasattr(count_response, 'count') else 0
        
        # Get paginated results
        response = supabase_admin.table("conversations")\
            .select("*")\
            .eq("user_id", user_id)\
            .eq("is_archived", archived)\
            .order("updated_at", desc=True)\
            .range(offset, offset + page_size - 1)\
            .execute()
        
        return response.data or [], total
    
    @staticmethod
    async def update(
        conversation_id: str,
        user_id: str,
        **updates
    ) -> Optional[Dict]:
        """Update conversation."""
        
        # Remove None values
        updates = {k: v for k, v in updates.items() if v is not None}
        
        response = supabase_admin.table("conversations")\
            .update(updates)\
            .eq("id", conversation_id)\
            .eq("user_id", user_id)\
            .execute()
        
        return response.data[0] if response.data else None
    
    @staticmethod
    async def delete(
        conversation_id: str,
        user_id: str,
        soft_delete: bool = True
    ) -> bool:
        """Delete or archive conversation."""
        
        if soft_delete:
            response = supabase_admin.table("conversations")\
                .update({"is_archived": True})\
                .eq("id", conversation_id)\
                .eq("user_id", user_id)\
                .execute()
        else:
            response = supabase_admin.table("conversations")\
                .delete()\
                .eq("id", conversation_id)\
                .eq("user_id", user_id)\
                .execute()
        
        return len(response.data) > 0
    
    @staticmethod
    async def get_messages(
        conversation_id: str,
        user_id: str,
        page: int = 1,
        page_size: int = 50,
    ) -> Tuple[List[Dict], int]:
        """Get messages for conversation."""
        
        # Verify ownership
        conversation = await ConversationService.get(conversation_id, user_id)
        if not conversation:
            return [], 0
        
        offset = (page - 1) * page_size
        
        # Get total count
        count_response = supabase_admin.table("messages")\
            .select("*", count="exact")\
            .eq("conversation_id", conversation_id)\
            .execute()
        
        total = count_response.count if hasattr(count_response, 'count') else 0
        
        # Get paginated messages
        response = supabase_admin.table("messages")\
            .select("*")\
            .eq("conversation_id", conversation_id)\
            .order("created_at")\
            .range(offset, offset + page_size - 1)\
            .execute()
        
        return response.data or [], total


conversation_service = ConversationService()