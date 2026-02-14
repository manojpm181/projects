from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from collections import defaultdict
import time

from src.core.config import settings


class InMemoryRateLimiter:
    """Simple in-memory rate limiter (FREE, no Redis)."""
    
    def __init__(self):
        self.requests = defaultdict(list)
    
    def check(self, key: str) -> tuple[bool, int]:
        """Check if request is within rate limit."""
        now = time.time()
        window = settings.RATE_LIMIT_PERIOD
        limit = settings.RATE_LIMIT_REQUESTS
        
        # Clean old requests
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if now - req_time < window
        ]
        
        # Check limit
        if len(self.requests[key]) >= limit:
            retry_after = int(window - (now - self.requests[key][0]))
            return False, retry_after
        
        # Add current request
        self.requests[key].append(now)
        remaining = limit - len(self.requests[key])
        
        return True, remaining


rate_limiter = InMemoryRateLimiter()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware using in-memory storage."""
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for certain paths
        if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
        
        # Get client identifier (IP address)
        client_ip = request.client.host if request.client else "unknown"
        
        # Check rate limit
        allowed, remaining_or_retry = rate_limiter.check(client_ip)
        
        if not allowed:
            return JSONResponse(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": f"Rate limit exceeded. Try again in {remaining_or_retry} seconds."
                },
                headers={
                    "Retry-After": str(remaining_or_retry),
                    "X-RateLimit-Limit": str(settings.RATE_LIMIT_REQUESTS),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time() + remaining_or_retry)),
                }
            )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_REQUESTS)
        response.headers["X-RateLimit-Remaining"] = str(remaining_or_retry)
        response.headers["X-RateLimit-Reset"] = str(int(time.time() + settings.RATE_LIMIT_PERIOD))
        
        return response