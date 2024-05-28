import os
from fastapi import FastAPI, Depends, HTTPException, Query, WebSocket
from fastapi_limiter.depends import RateLimiter
from fastapi_limiter import FastAPILimiter
from .services import get_equities_data
from aiocache import Cache
import redis.asyncio as redis
from fastapi.websockets import WebSocketDisconnect
import json
from dotenv import load_dotenv

load_dotenv() 

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    redis_pool = redis.ConnectionPool.from_url(redis_url)
    redis_conn = redis.Redis(connection_pool=redis_pool)
    await FastAPILimiter.init(redis_conn)
    Cache.REDIS = {
        'endpoint': redis_url.split('@')[-1].split(':')[0],
        'port': int(redis_url.split(':')[-1]),
        'serializer': {
            'class': "aiocache.serializers.JsonSerializer"
        }
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to the Financial API"}

@app.get("/equities-data", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_combined_data(stocks: list[str] = Query(None), cryptos: list[str] = Query(None)):
    data = await get_equities_data(stocks, cryptos)
    if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"])
    return data

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            request = json.loads(data)
            stocks = request.get("stocks", [])
            cryptos = request.get("cryptos", [])
            combined_data = await get_equities_data(stocks, cryptos)
            await websocket.send_json(combined_data)
    except WebSocketDisconnect:
        print("Client disconnected")
