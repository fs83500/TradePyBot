"""
Trades API
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.db import get_db
from backend.database.crud import CRUD
from backend.models.trade import Trade, TradeDirection, TradeStatus
from backend.config import settings
from datetime import datetime
from typing import List

router = APIRouter(prefix="/api/trades", tags=["trades"])


@router.get("/", response_model=List[Dict[str, Any]])
async def get_trades(
    status: str = None,
    symbol: str = None,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get trades history"""
    from sqlalchemy import select
    
    query = select(Trade)
    
    if status:
        query = query.where(Trade.status == status)
    if symbol:
        query = query.where(Trade.symbol == symbol)
    
    query = query.order_by(Trade.created_at.desc()).limit(limit)
    
    result = await db.execute(query)
    trades = result.scalars().all()
    
    return [{
        "id": t.id,
        "symbol": t.symbol,
        "direction": t.direction,
        "entry_price": t.entry_price,
        "exit_price": t.exit_price,
        "amount": t.amount,
        "profit": t.profit,
        "status": t.status,
        "agent_name": t.agent_name,
        "exchange": t.exchange,
        "created_at": t.created_at.isoformat(),
        "reason": t.reason
    } for t in trades]


@router.post("/", response_model=Dict[str, Any])
async def create_trade(
    symbol: str,
    direction: str,
    amount: float,
    agent_name: str = None,
    reason: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Create a new trade"""
    # Validate direction
    if direction not in ["long", "short"]:
        raise HTTPException(status_code=400, detail="Invalid direction. Use 'long' or 'short'")
    
    trade = Trade(
        symbol=symbol,
        direction=direction,
        entry_price=0.0,  # Will be set when executed
        amount=amount,
        status=TradeStatus.PENDING,
        agent_name=agent_name,
        reason=reason,
        created_at=datetime.now()
    )
    
    db_trade = await CRUD.create(db, trade)
    
    return {
        "id": db_trade.id,
        "symbol": db_trade.symbol,
        "direction": db_trade.direction,
        "amount": db_trade.amount,
        "status": db_trade.status,
        "agent_name": db_trade.agent_name,
        "created_at": db_trade.created_at.isoformat()
    }


@router.get("/{trade_id}", response_model=Dict[str, Any])
async def get_trade(trade_id: int, db: AsyncSession = Depends(get_db)):
    """Get trade by ID"""
    trade = await CRUD.get_by_id(db, Trade, trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    return {
        "id": trade.id,
        "symbol": trade.symbol,
        "direction": trade.direction,
        "entry_price": trade.entry_price,
        "exit_price": trade.exit_price,
        "amount": trade.amount,
        "profit": trade.profit,
        "status": trade.status,
        "agent_name": trade.agent_name,
        "created_at": trade.created_at.isoformat()
    }


@router.put("/{trade_id}/close")
async def close_trade(
    trade_id: int, 
    exit_price: float,
    db: AsyncSession = Depends(get_db)
):
    """Close a trade"""
    trade = await CRUD.get_by_id(db, Trade, trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    trade.exit_price = exit_price
    trade.profit = exit_price - trade.entry_price
    trade.status = TradeStatus.CLOSED
    trade.closed_at = datetime.now()
    
    await db.commit()
    await db.refresh(trade)
    
    return {
        "id": trade.id,
        "profit": trade.profit,
        "status": trade.status,
        "closed_at": trade.closed_at.isoformat()
    }
