from typing import Optional, Dict
from src.core.supabase import supabase, supabase_admin
from src.core.config import settings


class AuthService:
    """Authentication service using Supabase Auth (FREE)."""
    
    @staticmethod
    async def sign_up(email: str, password: str, full_name: Optional[str] = None) -> Dict:
        """Register new user."""
        try:
            response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name or email.split("@")[0],
                    }
                }
            })
            
            return {
                "user": response.user,
                "session": response.session,
            }
        except Exception as e:
            raise Exception(f"Registration failed: {str(e)}")
    
    @staticmethod
    async def sign_in(email: str, password: str) -> Dict:
        """Login user."""
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password,
            })
            
            return {
                "user": response.user,
                "session": response.session,
            }
        except Exception as e:
            raise Exception(f"Login failed: {str(e)}")
    
    @staticmethod
    async def sign_out(token: str) -> bool:
        """Logout user."""
        try:
            supabase.auth.sign_out()
            return True
        except Exception:
            return False
    
    @staticmethod
    async def refresh_session(refresh_token: str) -> Optional[Dict]:
        """Refresh session token."""
        try:
            response = supabase.auth.refresh_session(refresh_token)
            return {
                "user": response.user,
                "session": response.session,
            }
        except Exception:
            return None
    
    @staticmethod
    async def get_user(token: str) -> Optional[Dict]:
        """Get user from token."""
        try:
            response = supabase.auth.get_user(token)
            return response.user
        except Exception:
            return None
    
    @staticmethod
    async def get_profile(user_id: str) -> Optional[Dict]:
        """Get user profile from database."""
        try:
            response = supabase_admin.table("profiles")\
                .select("*")\
                .eq("id", user_id)\
                .execute()
            
            if response.data:
                return response.data[0]
            return None
        except Exception:
            return None


auth_service = AuthService()