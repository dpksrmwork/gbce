Global Beverage Corporation Exchange API
#  GBCE Stock Trading API

## 📖 Overview
This is a FastAPI-based stock trading API that allows users to manage stocks, execute trades, and compute financial metrics like **P/E ratio**, **Dividend Yield**, **Volume Weighted Stock Price (VWSP)**, and the **GBCE All Share Index**.

## 🚀 Features
- **Stock Management**: Create and fetch stock details.
- **Trade Management**: Record buy/sell trades.
- **Financial Calculations**:
  - P/E Ratio
  - Dividend Yield
  - Volume Weighted Stock Price
  - GBCE All Share Index


## ⚙️ Installation
Clone the Repository**
```sh
git clone https://github.com/dpksrmwork/gbce.git
cd gbce
```

###  Create a Virtual Environment & Install Dependencies**
```sh
python -m venv .venv
source .venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r app/requirements.txt
```

###  Run the API Server**
```sh
uvicorn app.src.main:app --host 0.0.0.0 --port 8080 --reload
```

##  API Endpoints

###  Stock Management**
| Method | Endpoint  | Description |
|--------|----------|-------------|
| `POST` | `/stocks/` | Create a new stock |
| `GET` | `/stocks/all_share_index` | Compute GBCE All Share Index |

###  Trade Management**
| Method | Endpoint  | Description |
|--------|----------|-------------|
| `POST` | `/trades/` | Record a new trade |

###  Financial Metrics**
| Method | Endpoint  | Description |
|--------|----------|-------------|
| `POST` | `/stocks/pe_ratio/` | Compute P/E Ratio |
| `POST` | `/stocks/dividend_yield/` | Compute Dividend Yield |
| `GET` | `/stocks/vwsp/` | Compute VWSP for a stock |

## 🛠️ Example Requests
### **Create a Stock**
```sh
curl -X POST "http://localhost:8080/stocks/" \
    -H "Content-Type: application/json" \
    -d '{
        "symbol": "AAPL",
        "stock_type": "Common",
        "last_dividend": 5,
        "par_value": 100
    }'
```

### **Create a Trade**
```sh
curl -X POST "http://localhost:8080/trades/" \
    -H "Content-Type: application/json" \
    -d '{
        "stock_symbol": "AAPL",
        "quantity": 10,
        "trade_type": "buy",
        "price": 150
    }'
```

### **Calculate VWSP**
```sh
curl -X POST "http://localhost:8080/stocks/vwsp/" \
    -H "Content-Type: application/json" \
    -d '{"symbol": "AAPL"}'
```

##  API Documentation
After running the server, access Swagger UI:
- **Swagger UI**: [http://localhost:8080/docs](http://localhost:8080/docs)
- **ReDoc**: [http://localhost:8080/redoc](http://localhost:8080/redoc)

