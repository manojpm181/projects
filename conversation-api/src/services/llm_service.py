from typing import List, Dict, AsyncGenerator, Optional
import time
import uuid

from src.llm.groq_client import groq_client
from src.llm.token_counter import token_counter
from src.llm.prompts import Prompts
from src.core.config import settings


class LLMService:
    """Free LLM service using Groq."""
    
    def __init__(self):
        self.client = groq_client
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
        model: str = settings.DEFAULT_MODEL,
        temperature: float = settings.TEMPERATURE,
        max_tokens: int = settings.MAX_TOKENS,
    ) -> Dict | AsyncGenerator:
        """Generate response using Groq free tier."""
        
        start_time = time.time()
        
        try:
            if stream:
                return self._stream_response(
                    messages, model, temperature, max_tokens, start_time
                )
            
            # Non-streaming
            response = await self.client.chat_completion(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False,
            )
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            # Extract response content
            choice = response["choices"][0]
            content = choice["message"]["content"]
            finish_reason = choice.get("finish_reason", "stop")
            
            # Count tokens
            input_text = " ".join([m.get("content", "") for m in messages])
            input_tokens = await self.client.count_tokens(input_text)
            output_tokens = await self.client.count_tokens(content)
            
            return {
                "content": content,
                "finish_reason": finish_reason,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
                "model": response["model"],
                "latency_ms": latency_ms,
                "id": response["id"],
            }
            
        except Exception as e:
            raise Exception(f"LLM generation failed: {str(e)}")
    
    async def _stream_response(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: int,
        start_time: float,
    ) -> AsyncGenerator[Dict, None]:
        """Stream response from Groq."""
        
        try:
            stream = await self.client.chat_completion(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            
            full_content = []
            finish_reason = None
            response_id = None
            
            async for chunk in stream:
                if chunk.get("choices"):
                    choice = chunk["choices"][0]
                    
                    # Get delta content
                    if choice.get("delta", {}).get("content"):
                        delta = choice["delta"]["content"]
                        full_content.append(delta)
                        
                        yield {
                            "type": "delta",
                            "content": delta,
                            "finish_reason": None,
                        }
                    
                    # Get finish reason
                    if choice.get("finish_reason"):
                        finish_reason = choice["finish_reason"]
                    
                    # Get response ID
                    if chunk.get("id"):
                        response_id = chunk["id"]
            
            # Calculate final stats
            latency_ms = int((time.time() - start_time) * 1000)
            full_text = "".join(full_content)
            output_tokens = await self.client.count_tokens(full_text)
            
            yield {
                "type": "complete",
                "content": full_text,
                "finish_reason": finish_reason or "stop",
                "output_tokens": output_tokens,
                "model": model,
                "latency_ms": latency_ms,
                "id": response_id or str(uuid.uuid4()),
            }
            
        except Exception as e:
            yield {
                "type": "error",
                "error": str(e),
            }
    
    async def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return await self.client.count_tokens(text)


# Global LLM service instance
llm_service = LLMService()