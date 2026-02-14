import httpx
from typing import AsyncGenerator, List, Dict, Optional
import time
import json

from src.core.config import settings


class GroqFreeClient:
    """Groq API client - 100% FREE tier."""
    
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1"
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = settings.DEFAULT_MODEL,
        temperature: float = settings.TEMPERATURE,
        max_tokens: int = settings.MAX_TOKENS,
        stream: bool = False,
    ) -> Dict | AsyncGenerator:
        """Chat completion with Groq (supports streaming)."""
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }
        
        if stream:
            return self._stream_completion(payload, model)
        
        # Non-streaming
        response = await self.client.post(
            f"{self.base_url}/chat/completions",
            json=payload,
        )
        
        if response.status_code != 200:
            error_text = await response.aread()
            raise Exception(f"Groq API error: {error_text.decode()}")
        
        return response.json()
    
    async def _stream_completion(
        self,
        payload: Dict,
        model: str,
    ) -> AsyncGenerator[Dict, None]:
        """Stream completion from Groq."""
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                json=payload,
                headers={"Authorization": f"Bearer {self.api_key}"},
            ) as response:
                
                if response.status_code != 200:
                    error_text = await response.aread()
                    raise Exception(f"Groq streaming error: {error_text.decode()}")
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        
                        if data.strip() == "[DONE]":
                            break
                        
                        try:
                            chunk = json.loads(data)
                            yield chunk
                        except json.JSONDecodeError:
                            continue
    
    async def count_tokens(self, text: str) -> int:
        """Approximate token count (free, no tiktoken)."""
        # Simple approximation: 1 token ≈ 4 characters for English
        return len(text) // 4
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()


# Global Groq client instance
groq_client = GroqFreeClient()