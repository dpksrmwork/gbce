import uvicorn
from fastapi import FastAPI
from app.src.api.stocks import router as stock_router
from app.src.api.trades import router as trade_router
from app.src.services.gbc_db import init_db

# Initialize FastAPI app
app = FastAPI(title="GBCE Stock Market API")

# Initialize the database
init_db()

# Include routers
app.include_router(stock_router, prefix="/stocks", tags=["Stocks"])
app.include_router(trade_router, prefix="/trades", tags=["Trades"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)