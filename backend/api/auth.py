"""
Auth API - Token authentication (comme OpenClaw gateway)
"""

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.db import get_db
from backend.database.crud import CRUD
from backend.models.user import User
from backend.config import settings
from datetime import datetime, timedelta
import hashlib
import secrets

router = APIRouter(prefix="/api/auth", tags=["auth"])


def generate_token() -> str:
    """Generate a secure token"""
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    """Hash token for storage"""
    return hashlib.sha256(token.encode()).hexdigest()


async def verify_token(authorization: str = Header(None)) -> User:
    """Verify token and return user"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    # Extract token from "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    token_hash = hash_token(parts[1])
    
    async with get_db() as db:
        user = await CRUD.get_by_field(db, User, "token_hash", token_hash)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Check expiry
        if user.token_expiry and datetime.now() > user.token_expiry:
            raise HTTPException(status_code=401, detail="Token expired")
        
        return user


@router.post("/login")
async def login():
    """
    Login with token (comme OpenClaw gateway)
    
    Returns:
        {
            "token": str,
            "user": str,
            "expires_at": datetime
        }
    """
    # Generate token
    token = generate_token()
    token_hash = hash_token(token)
    
    # Calculate expiry
    expires_at = datetime.now() + timedelta(hours=settings.auth.token_expiry_hours)
    
    # Create/update user
    async with get_db() as db:
        user = await CRUD.get_by_field(db, User, "username", "trader")
        
        if not user:
            user = User(
                username="trader",
                token_hash=token_hash,
                token_expiry=expires_at,
                role="admin",
                is_active=1
            )
            db.add(user)
        else:
            user.token_hash = token_hash
            user.token_expiry = expires_at
            user.last_login = datetime.now()
        
        await db.commit()
        await db.refresh(user)
    
    return {
        "token": token,
        "user": user.username,
        "expires_at": user.token_expiry.isoformat()
    }


@router.get("/me")
async def get_me(user: User = Depends(verify_token)):
    """Get current user info"""
    return {
        "username": user.username,
        "role": user.role,
        "is_active": bool(user.is_active),
        "last_login": user.last_login.isoformat() if user.last_login else None
    }


@router.post("/logout")
async def logout(authorization: str = Header(None)):
    """Logout (invalidate token)"""
    if not authorization:
        return {"message": "Already logged out"}
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return {"message": "Invalid authorization format"}
    
    token_hash = hash_token(parts[1])
    
    async with get_db() as db:
        user = await CRUD.get_by_field(db, User, "token_hash", token_hash)
        if user:
            user.token_hash = None
            user.token_expiry = None
            await db.commit()
    
    return {"message": "Logged out successfully"}
