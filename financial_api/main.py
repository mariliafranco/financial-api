import os
from fastapi import FastAPI, HTTPException, Query, WebSocket, Depends
from fastapi_limiter.depends import RateLimiter
from fastapi_limiter import FastAPILimiter
from .services import get_equities_data
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

@app.get("/")
def read_root():
    return {"message": "Welcome to the Financial API"}

@app.get("/equities-data", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_combined_data(stocks: str = Query(None), cryptos: str = Query(None)):
    try:
        stock_list = stocks.split(",") if stocks else []
        crypto_list = cryptos.split(",") if cryptos else []
        data = await get_equities_data(stock_list, crypto_list)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        return data
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            request = json.loads(data)
            stocks = request.get("stocks", "")
            cryptos = request.get("cryptos", "")
            stock_list = stocks.split(",") if stocks else []
            crypto_list = cryptos.split(",") if cryptos else []
            combined_data = await get_equities_data(stock_list, crypto_list)
            await websocket.send_json(combined_data)
    except WebSocketDisconnect:
        print("Client disconnected")
