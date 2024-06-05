import os
import httpx
import asyncio
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"


async def get_stock_data(symbol: str):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        print(f"Request URL for {symbol}: {url}")  
        print(f"Response Data for {symbol}: {data}")  
        if 'Error Message' in data:
            print(f"Error fetching data for {symbol}: {data['Error Message']}")
            return {symbol: {"error": data['Error Message']}}
        
        # Extract ONLY the most recent daily data
        time_series = data.get("Time Series (Daily)", {})
        if time_series:
            most_recent_date = max(time_series.keys(), key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
            most_recent_data = time_series[most_recent_date]
            return {symbol: {most_recent_date: most_recent_data}}
        else:
            return {symbol: {"error": "No time series data available"}}

async def get_crypto_data(crypto: str):
    url = f"{COINGECKO_API_URL}/coins/markets?vs_currency=usd&ids={crypto}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        print(f"Request URL: {url}")  
        print(f"Response Data: {data}")  
        if not data:
            return {crypto: {"error": "No data available"}}
        crypto_info = data[0]
        filtered_data = {
            "id": crypto_info["id"],
            "symbol": crypto_info["symbol"],
            "name": crypto_info["name"],
            "current_price": crypto_info["current_price"],
            "market_cap": crypto_info["market_cap"],
            "total_volume": crypto_info["total_volume"],
            "high_24h": crypto_info["high_24h"],
            "low_24h": crypto_info["low_24h"],
            "price_change_percentage_24h": crypto_info["price_change_percentage_24h"],
            "last_updated": crypto_info["last_updated"]
        }
        return {crypto: filtered_data}

async def get_equities_data(stocks: list[str] = None, cryptos: list[str] = None):
    result = {}

    if not stocks and not cryptos:
        return {"error": "At least one of 'stocks' or 'cryptos' must be provided"}

    # Fetch each stock and crypto data
    stock_tasks = [get_stock_data(stock) for stock in stocks] if stocks else []
    crypto_tasks = [get_crypto_data(crypto) for crypto in cryptos] if cryptos else []

    # Return results from all data as our api response
    stock_results = await asyncio.gather(*stock_tasks) if stock_tasks else []
    crypto_results = await asyncio.gather(*crypto_tasks) if crypto_tasks else []

    if stocks:
        result["stock_data"] = {stock: data for stock_result in stock_results for stock, data in stock_result.items()}
    if cryptos:
        result["crypto_data"] = {crypto: data for crypto_result in crypto_results for crypto, data in crypto_result.items()}

    return result
