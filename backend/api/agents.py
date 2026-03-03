"""
Agents API
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.db import get_db
from backend.database.crud import CRUD
from backend.models.agent import Agent
from backend.agents.provider import AIProviders
from backend.agents.heliox import HelioxAgent
from backend.agents.syntax import SyntaxAgent
from backend.agents.prisme import PrismeAgent
from backend.config import settings
from datetime import datetime
from typing import List, Dict, Any

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.get("/", response_model=List[Dict[str, Any]])
async def get_agents(db: AsyncSession = Depends(get_db)):
    """Get all agents"""
    from sqlalchemy import select
    
    query = select(Agent)
    result = await db.execute(query)
    agents = result.scalars().all()
    
    return [{
        "id": a.id,
        "name": a.name,
        "provider": a.provider,
        "model": a.model,
        "strategy": a.strategy,
        "risk_level": a.risk_level,
        "risk_slider_value": a.risk_slider_value,
        "is_active": bool(a.is_active)
    } for a in agents]


@router.post("/", response_model=Dict[str, Any])
async def create_agent(
    name: str,
    provider: str,
    model: str,
    strategy: str = "momentum",
    db: AsyncSession = Depends(get_db)
):
    """Create a new agent"""
    # Validate provider
    if provider not in AIProviders.get_provider_names():
        raise HTTPException(status_code=400, detail=f"Invalid provider: {provider}")
    
    # Validate strategy
    valid_strategies = ["momentum", "mean_reversion", "sentiment"]
    if strategy not in valid_strategies:
        raise HTTPException(status_code=400, detail=f"Invalid strategy: {strategy}")
    
    # Create agent
    agent = Agent(
        name=name,
        provider=provider,
        model=model,
        strategy=strategy,
        risk_level="medium",
        risk_slider_value=0.5,
        is_active=1,
        created_at=datetime.now()
    )
    
    db_agent = await CRUD.create(db, agent)
    
    return {
        "id": db_agent.id,
        "name": db_agent.name,
        "provider": db_agent.provider,
        "model": db_agent.model,
        "strategy": db_agent.strategy,
        "risk_level": db_agent.risk_level,
        "risk_slider_value": db_agent.risk_slider_value
    }


@router.get("/{name}", response_model=Dict[str, Any])
async def get_agent(name: str, db: AsyncSession = Depends(get_db)):
    """Get agent by name"""
    from sqlalchemy import select
    query = select(Agent).where(Agent.name == name)
    result = await db.execute(query)
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {
        "id": agent.id,
        "name": agent.name,
        "provider": agent.provider,
        "model": agent.model,
        "strategy": agent.strategy,
        "risk_level": agent.risk_level,
        "risk_slider_value": agent.risk_slider_value
    }


@router.post("/{name}/configure")
async def configure_agent(
    name: str,
    risk_slider_value: float,
    db: AsyncSession = Depends(get_db)
):
    """Configure agent with risk slider"""
    from sqlalchemy import select
    query = select(Agent).where(Agent.name == name)
    result = await db.execute(query)
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Map slider 0-1 to risk levels
    if risk_slider_value < 0.33:
        risk_level = "low"
    elif risk_slider_value < 0.66:
        risk_level = "medium"
    else:
        risk_level = "high"
    
    agent.risk_level = risk_level
    agent.risk_slider_value = risk_slider_value
    agent.last_active = datetime.now()
    
    await db.commit()
    await db.refresh(agent)
    
    return {
        "id": agent.id,
        "name": agent.name,
        "risk_level": risk_level,
        "risk_slider_value": risk_slider_value
    }


@router.get("/providers")
async def list_providers():
    """List available AI providers"""
    return {
        "providers": AIProviders.PROVIDERS,
        "available": AIProviders.get_provider_names()
    }


@router.get("/providers/{provider}/models")
async def get_provider_models(provider: str):
    """Get models for a provider"""
    models = AIProviders.get_models(provider)
    
    if not models:
        raise HTTPException(status_code=404, detail=f"Provider not found: {provider}")
    
    return {"provider": provider, "models": models}
