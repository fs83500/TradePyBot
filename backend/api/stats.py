"""
Stats API
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.database.db import get_db
from backend.models.trade import Trade
from backend.models.agent import Agent
from datetime import datetime, timedelta
from typing import Dict, Any, List

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/", response_model=Dict[str, Any])
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Get overall statistics"""
    # Get total trades
    trades_query = select(func.count(Trade.id))
    trades_result = await db.execute(trades_query)
    total_trades = trades_result.scalar() or 0
    
    # Get total profit
    profit_query = select(func.sum(Trade.profit))
    profit_result = await db.execute(profit_query)
    total_profit = profit_result.scalar() or 0.0
    
    # Get win rate
    winning_query = select(func.count(Trade.id)).where(Trade.profit > 0)
    winning_result = await db.execute(winning_query)
    winning_trades = winning_result.scalar() or 0
    
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    
    # Get agents stats
    agents_query = select(Agent)
    agents_result = await db.execute(agents_query)
    agents = agents_result.scalars().all()
    
    agents_stats = [{
        "name": a.name,
        "win_rate": (a.accuracy * 100) if a.accuracy else 0,
        "risk_level": int(a.risk_slider_value * 10),
        "total_profit": a.total_profit or 0.0,
        "total_trades": a.total_predictions or 0
    } for a in agents]
    
    # Get best and worst trades
    best_trade_query = select(Trade).order_by(Trade.profit.desc()).limit(1)
    best_trade_result = await db.execute(best_trade_query)
    best_trade = best_trade_result.scalar_one_or_none()
    
    worst_trade_query = select(Trade).order_by(Trade.profit.asc()).limit(1)
    worst_trade_result = await db.execute(worst_trade_query)
    worst_trade = worst_trade_result.scalar_one_or_none()
    
    return {
        "total_trades": total_trades,
        "total_profit": total_profit,
        "win_rate": win_rate,
        "winning_trades": winning_trades,
        "agents": agents_stats,
        "best_trade": {
            "symbol": best_trade.symbol,
            "pnl": best_trade.profit,
            "agent": best_trade.agent_name
        } if best_trade else None,
        "worst_trade": {
            "symbol": worst_trade.symbol,
            "pnl": worst_trade.profit,
            "agent": worst_trade.agent_name
        } if worst_trade else None,
        "monthly_performance": [
            {"month": "Jan", "value": 60},
            {"month": "Feb", "value": 75},
            {"month": "Mar", "value": 45},
            {"month": "Apr", "value": 80},
            {"month": "May", "value": 55},
            {"month": "Jun", "value": 90},
            {"month": "Jul", "value": 70},
            {"month": "Aug", "value": 85}
        ]
    }


@router.get("/portfolio", response_model=Dict[str, Any])
async def get_portfolio_stats(db: AsyncSession = Depends(get_db)):
    """Get portfolio statistics"""
    # Get portfolio summary
    trades_query = select(func.count(Trade.id))
    trades_result = await db.execute(trades_query)
    total_trades = trades_result.scalar() or 0
    
    profit_query = select(func.sum(Trade.profit))
    profit_result = await db.execute(profit_query)
    total_profit = profit_result.scalar() or 0.0
    
    # Calculate balance (demo)
    initial_balance = 10000.0
    current_balance = initial_balance + total_profit
    
    return {
        "balance": current_balance,
        "pnl": total_profit,
        "win_rate": 68.5,  # Demo value
        "active_trades": 4,  # Demo value
        "total_trades": total_trades
    }


@router.get("/feedback", response_model=List[Dict[str, Any]])
async def get_recent_feedback(
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """Get recent AI feedback"""
    # Return demo feedback for now
    return [
        {
            "agent": "heliox",
            "message": "BTC showed strong momentum signals. Entered long position with tight stop-loss. Risk level 8/10 suitable for this aggressive trade.",
            "timestamp": (datetime.now() - timedelta(minutes=2)).isoformat()
        },
        {
            "agent": "syntax",
            "message": "ETH price deviated from mean by 2.5 standard deviations. Mean reversion strategy suggests selling. Risk level 5/10 maintained.",
            "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat()
        },
        {
            "agent": "prisme",
            "message": "News sentiment for AAPL turned positive after earnings beat. Conservative entry with small position size. Risk level 3/10 appropriate.",
            "timestamp": (datetime.now() - timedelta(hours=1)).isoformat()
        }
    ][:limit]