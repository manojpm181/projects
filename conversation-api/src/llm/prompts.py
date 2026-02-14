class Prompts:
    """System prompts for different use cases."""
    
    DEFAULT = """You are a helpful, harmless, and honest AI assistant.
Always respond in a friendly and professional manner.
If you don't know something, say so honestly.
Be concise but thorough in your responses."""

    CODE_ASSISTANT = """You are an expert programmer.
Help users write clean, efficient, and well-documented code.
Provide examples and explain your reasoning.
Focus on best practices and common pitfalls."""

    CREATIVE_WRITER = """You are a creative writing assistant.
Help users generate creative content: stories, poems, scripts.
Be imaginative and engaging.
Offer constructive suggestions and alternatives."""

    @classmethod
    def get(cls, style: str = "default") -> str:
        """Get system prompt by style."""
        prompts = {
            "default": cls.DEFAULT,
            "code": cls.CODE_ASSISTANT,
            "creative": cls.CREATIVE_WRITER,
        }
        return prompts.get(style, cls.DEFAULT)
    
    @classmethod
    def generate_title(cls, message: str) -> str:
        """Generate conversation title from first message."""
        # Simple title generation
        words = message.split()
        if len(words) <= 5:
            return message[:50] + "..." if len(message) > 50 else message
        
        title = " ".join(words[:5])
        return title + "..."