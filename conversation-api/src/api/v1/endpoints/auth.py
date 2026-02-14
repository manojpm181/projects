from fastapi import APIRouter, HTTPException, Depends, status
from src.api.v1.schemas.auth import (
    UserCreate, UserLogin, UserResponse, TokenResponse, ProfileResponse
)
from src.services.auth_service import auth_service
from src.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register new user with Supabase Auth (FREE)."""
    try:
        result = await auth_service.sign_up(
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
        )
        
        return TokenResponse(
            access_token=result["session"].access_token,
            refresh_token=result["session"].refresh_token,
            token_type="bearer",
            expires_in=result["session"].expires_in,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin):
    """Login with Supabase Auth (FREE)."""
    try:
        result = await auth_service.sign_in(
            email=user_data.email,
            password=user_data.password,
        )
        
        return TokenResponse(
            access_token=result["session"].access_token,
            refresh_token=result["session"].refresh_token,
            token_type="bearer",
            expires_in=result["session"].expires_in,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """Refresh access token."""
    try:
        result = await auth_service.refresh_session(refresh_token)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        return TokenResponse(
            access_token=result["session"].access_token,
            refresh_token=result["session"].refresh_token,
            token_type="bearer",
            expires_in=result["session"].expires_in,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(token: str = Depends(get_current_user)):
    """Logout user."""
    await auth_service.sign_out(token)
    return None


@router.get("/me", response_model=ProfileResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user profile."""
    profile = await auth_service.get_profile(current_user["id"])
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile