from typing import Dict, List


class TokenCounter:
    """Simple token counter - 100% free, no external dependencies."""
    
    @staticmethod
    def count(text: str) -> int:
        """
        Approximate token count for English text.
        ~4 characters per token average.
        """
        if not text:
            return 0
        return len(text) // 4
    
    @staticmethod
    def truncate(text: str, max_tokens: int) -> str:
        """Truncate text to approximate token limit."""
        if TokenCounter.count(text) <= max_tokens:
            return text
        
        # Rough truncation: 4 chars per token
        max_chars = max_tokens * 4
        return text[:max_chars] + "..."
    
    @staticmethod
    def truncate_messages(
        messages: List[Dict[str, str]],
        max_tokens: int = 4000
    ) -> List[Dict[str, str]]:
        """Truncate conversation history to fit token limit."""
        
        total_tokens = 0
        truncated = []
        
        # Process in reverse (keep recent messages)
        for msg in reversed(messages):
            msg_tokens = TokenCounter.count(msg.get("content", ""))
            
            if total_tokens + msg_tokens > max_tokens:
                # Truncate this message
                remaining = max_tokens - total_tokens
                if remaining > 50:
                    msg["content"] = TokenCounter.truncate(
                        msg["content"],
                        remaining
                    )
                    truncated.insert(0, msg)
                break
            
            total_tokens += msg_tokens
            truncated.insert(0, msg)
        
        return truncated


token_counter = TokenCounter()