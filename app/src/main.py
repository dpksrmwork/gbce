import time
import uvicorn
from fastapi import FastAPI, Request
from app.src.utils.logger import logger
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


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log all incoming requests and responses."""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    logger.info(
        f"{request.method} {request.url.path} - Status: {response.status_code} - Duration: {duration:.3f}s"
    )
    
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)