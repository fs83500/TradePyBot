"""
WebSocket API for real-time data
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set, Any
import asyncio
import json

router = APIRouter(tags=["websocket"])

# WebSocket connections
market_connections: Dict[str, Set[WebSocket]] = {}
feedback_connections: Set[WebSocket] = set()


@router.websocket("/ws/market/{symbol}")
async def market_websocket(websocket: WebSocket, symbol: str):
    """WebSocket for market data (prices, OHLCV)"""
    await websocket.accept()
    
    if symbol not in market_connections:
        market_connections[symbol] = set()
    market_connections[symbol].add(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "subscribe":
                await websocket.send_text(json.dumps({
                    "type": "subscribed",
                    "symbol": symbol
                }))
            
            elif message.get("type") == "ping":
                await websocket.send_text(json.dumps({
                    "type": "pong",
                    "timestamp": asyncio.get_event_loop().time()
                }))
            
            await asyncio.sleep(1)
    
    except WebSocketDisconnect:
        market_connections[symbol].discard(websocket)
        if not market_connections[symbol]:
            del market_connections[symbol]


@router.websocket("/ws/feedback")
async def feedback_websocket(websocket: WebSocket):
    """WebSocket for AI feedback stream"""
    await websocket.accept()
    feedback_connections.add(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "ping":
                await websocket.send_text(json.dumps({
                    "type": "pong",
                    "timestamp": asyncio.get_event_loop().time()
                }))
            
            await asyncio.sleep(5)
    
    except WebSocketDisconnect:
        feedback_connections.discard(websocket)


async def broadcast_market_data(symbol: str, data: Dict[str, Any]):
    """Broadcast market data to all subscribers"""
    if symbol not in market_connections:
        return
    
    message = json.dumps({
        "type": "market_data",
        "symbol": symbol,
        "data": data,
        "timestamp": asyncio.get_event_loop().time()
    })
    
    for connection in list(market_connections[symbol]):
        try:
            await connection.send_text(message)
        except Exception:
            market_connections[symbol].discard(connection)


async def broadcast_feedback(feedback: Dict[str, Any]):
    """Broadcast feedback to all subscribers"""
    message = json.dumps({
        "type": "feedback",
        "data": feedback,
        "timestamp": asyncio.get_event_loop().time()
    })
    
    for connection in list(feedback_connections):
        try:
            await connection.send_text(message)
        except Exception:
            feedback_connections.discard(connection)
