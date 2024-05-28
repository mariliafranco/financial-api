import os
import httpx
from aiocache import Cache, cached
import asyncio
from dotenv import load_dotenv

load_dotenv()  

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

@cached(ttl=3600, cache=Cache.REDIS)
async def get_stock_data(symbol: str):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

@cached(ttl=3600, cache=Cache.REDIS)
async def get_crypto_data(crypto: str):
    url = f"{COINGECKO_API_URL}/coins/markets?vs_currency=usd&ids={crypto}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

async def get_equities_data(stocks: list[str] = None, cryptos: list[str] = None):
    result = {}

    if not stocks and not cryptos:
        return {"error": "At least one of 'stocks' or 'cryptos' must be provided"}

    stock_tasks = [get_stock_data(stock) for stock in stocks] if stocks else []
    crypto_tasks = [get_crypto_data(crypto) for crypto in cryptos] if cryptos else []

    results = await asyncio.gather(*stock_tasks, *crypto_tasks)

    if stocks:
        result["stock_data"] = results[:len(stocks)]
    if cryptos:
        result["crypto_data"] = results[len(stocks):]

    return result
