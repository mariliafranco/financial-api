# Financial API 🪙📈

A FastAPI-based service providing real-time and historical data for stocks and cryptocurrencies. This API aggregates data from multiple sources to offer comprehensive financial information. Ideal for integration with web applications, mobile apps, and Chrome extensions.

## Features

- Real-time stock data from Alpha Vantage
- Cryptocurrency data from CoinGecko
- Combined data endpoint for stocks and cryptocurrencies
<!-- - Rate limiting to manage API usage -->
- WebSocket support for real-time updates

## Setup

1. **Clone the repository:**

```bash
git clone https://github.com/mariliafranco/financial-api.git
cd financial-api
```

2. **(Optional) Create and activate a virtual environment:**

### For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### For Linux or MacOS:

```bash
python -m venv venv
source venv/bin/activate
```

3. **Install Dependencies:**

### If you are using Poetry:

```bash
poetry install
```

### If you are using pip:

```bash
pip install -r requirements.txt
```

4. **Create a `.env` file:**

Claim your Alpha Vantage API key on `https://www.alphavantage.co/support/#api-key`

Replace `your_alpha_vantage_api_key` with this generated Alpha Vantage API key  
_ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_

## Running the API Locally

1. **Start the FastAPI Server:**

```bash
uvicorn financial_api.main:app --reload
```

2. **Access the API documentation:**
   Open your browser and navigate to `http://127.0.0.1:8000/docs`.

## Endpoints

### Fetch Equities and Crypto Data

- **URL:** `/equities-data`
- **Method:** `GET`
- **Query Parameters:**
  - `stocks` (optional): Comma-separated list of stock symbols (e.g., `AAPL,GOOGL`)
  - `cryptos` (optional): Comma-separated list of cryptocurrency IDs (e.g., `bitcoin,ethereum`)

**Example Request:**

```bash
curl -X GET "http://127.0.0.1:8000/equities-data?stocks=AAPL,GOOGL&cryptos=bitcoin,ethereum"
```

**Example Response:**

```json
{
  "stock_data": {
    "AAPL": {
      "2024-06-06": {
        "open": "181.5300",
        "high": "183.7900",
        "low": "181.4500",
        "close": "183.3100",
        "volume": "53752440"
      }
    },
    "GOOGL": {
      "2024-06-06": {
        "open": "139.4700",
        "high": "140.7900",
        "low": "138.9500",
        "close": "140.3100",
        "volume": "17152740"
      }
    }
  },
  "crypto_data": {
    "bitcoin": {
      "symbol": "btc",
      "name": "Bitcoin",
      "current_price": 71329,
      "market_cap": 1405702965510,
      "total_volume": 28346592593,
      "high_24h": 71741,
      "low_24h": 70062,
      "price_change_percentage_24h": 0.78893,
      "last_updated": "2024-06-05T16:59:45.012Z"
    },
    "ethereum": {
      "symbol": "eth",
      "name": "Ethereum",
      "current_price": 3798.43,
      "market_cap": 456340049667,
      "total_volume": 12483706194,
      "high_24h": 3839.32,
      "low_24h": 3776.87,
      "price_change_percentage_24h": -0.41035,
      "last_updated": "2024-06-05T16:59:36.254Z"
    }
  }
}
```

## Deployment

This project is configured for deployment on Vercel, which calls for your project to be connected to your GitHub repository.

1. **Push your code to GitHub:**

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy on Vercel:**

- Ensure you have a `vercel.json` file with the appropriate configuration.
- Go to the Vercel dashboard and connect your repository.
- Set the environment variables, including `ALPHA_VANTAGE_API_KEY`.

Vercel will automatically detect the changes and redeploy your project.

## License

This project is licensed under the MIT License.  
_But that is going to change very soon_ 💅🏻
