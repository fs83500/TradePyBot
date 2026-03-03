"""
Portfolio API
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.db import get_db
from backend.database.crud import CRUD
from backend.models.portfolio import Portfolio
from datetime import datetime
from typing import List

router = APIRouter(prefix="/api/portfolio", tags=["portfolio"])


@router.get("/", response_model=List[Dict[str, Any]])
async def get_portfolios(db: AsyncSession = Depends(get_db)):
    """Get all portfolios"""
    from sqlalchemy import select
    
    query = select(Portfolio)
    result = await db.execute(query)
    portfolios = result.scalars().all()
    
    return [{
        "id": p.id,
        "name": p.name,
        "type": p.type,
        "initial_balance": p.initial_balance,
        "current_balance": p.current_balance,
        "free_balance": p.free_balance,
        "total_trades": p.total_trades,
        "is_active": bool(p.is_active)
    } for p in portfolios]


@router.post("/", response_model=Dict[str, Any])
async def create_portfolio(
    name: str,
    initial_balance: float = 1000.0,
    db: AsyncSession = Depends(get_db)
):
    """Create a new portfolio"""
    portfolio = Portfolio(
        name=name,
        initial_balance=initial_balance,
        current_balance=initial_balance,
        free_balance=initial_balance,
        type="paper",
        is_active=1,
        created_at=datetime.now()
    )
    
    db_portfolio = await CRUD.create(db, portfolio)
    
    return {
        "id": db_portfolio.id,
        "name": db_portfolio.name,
        "initial_balance": db_portfolio.initial_balance,
        "current_balance": db_portfolio.current_balance
    }


@router.get("/{name}", response_model=Dict[str, Any])
async def get_portfolio(name: str, db: AsyncSession = Depends(get_db)):
    """Get portfolio by name"""
    from sqlalchemy import select
    query = select(Portfolio).where(Portfolio.name == name)
    result = await db.execute(query)
    portfolio = result.scalar_one_or_none()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    return {
        "id": portfolio.id,
        "name": portfolio.name,
        "initial_balance": portfolio.initial_balance,
        "current_balance": portfolio.current_balance,
        "total_trades": portfolio.total_trades,
        "winning_trades": portfolio.winning_trades
    }
