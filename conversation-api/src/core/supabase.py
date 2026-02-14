from supabase import create_client, Client
from src.core.config import settings

# Supabase client (free tier)
supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_ANON_KEY
)

# Admin client (for service role operations)
supabase_admin: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_ROLE_KEY
)


async def get_supabase() -> Client:
    """Dependency to get Supabase client."""
    return supabase


async def get_supabase_admin() -> Client:
    """Dependency to get Supabase admin client."""
    return supabase_admin