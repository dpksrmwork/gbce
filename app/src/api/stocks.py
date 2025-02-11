import uuid
from fastapi import APIRouter, HTTPException
from app.src.models.stock import Stock
from app.src.models.api_requests import PriceRequest
from app.src.services.gbc_db import add_stock, get_stock, get_trades_for_stock
from app.src.utils.helper import calculate_dividend_yield, calculate_pe_ratio, calculate_gbce_all_share_index, volume_weighted_stock_price
from app.src.utils.audit_helper import generate_transaction_id

router = APIRouter()


@router.post("/", response_model=dict)
def create_stock(stock: Stock):
    """
    Create a new stock entry.

    - Ensures stock symbol uniqueness.
    - Returns a persistent UUID as a transaction ID.
    """

    existing_stock = get_stock(stock.symbol)
    if existing_stock:
        raise HTTPException(status_code=400, detail="Stock with this symbol already exists.")

    # Generate a unique transaction ID only once per stock creation
    transaction_id = generate_transaction_id()

    add_stock(stock)

    return {
        "transaction_id": transaction_id,
        "message": "Stock added successfully",
        "stock_symbol": stock.symbol
    }

@router.post("/dividend_yield/", response_model=dict)
def get_dividend(request: PriceRequest):
    transaction_id = generate_transaction_id()

    stock = get_stock(request.symbol)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    try:
        dividend_yield = calculate_dividend_yield(stock, request.price)
        return {
            "transaction_id": transaction_id,
            "stock_symbol": request.symbol,
            "dividend_yield": dividend_yield
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pe_ratio/", response_model=dict)
def get_pe_ratio(request: PriceRequest):

    transaction_id = generate_transaction_id()
    stock = get_stock(request.symbol)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    try:
        pe_ratio = calculate_pe_ratio(stock, request.price)
        return {
            "transaction_id": transaction_id,
            "symbol": request.symbol,
            "pe_ratio": pe_ratio}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.get("/vwsp/", response_model=dict)
def get_vwsp(request: dict):
    """
    Get the Volume Weighted Stock Price (VWSP) for a given stock.
    - VWSP = (Sum of (Price * Quantity)) / (Sum of Quantities)
    - Defaults to last 5 minutes of trades.
    """
    transaction_id = generate_transaction_id()
    symbol = request.get('symbol')
    trades = get_trades_for_stock(symbol)  # Fetch trades for the given stock
    if not trades:
        raise HTTPException(status_code=404, detail="No trades found for this stock")
    
    vwsp = volume_weighted_stock_price(trades)
    return {
        "transaction_id": transaction_id,
        "symbol": symbol,
        "vwsp": vwsp}


@router.get("/all_share_index", response_model=dict)
def get_all_share_index():
    """
    API endpoint to fetch the GBCE All Share Index.

    :return: JSON response with the GBCE All Share Index.
    """
    transaction_id = generate_transaction_id()
    index_value = calculate_gbce_all_share_index()
    return {
        "transaction_id": transaction_id,
        "GBCE_All_Share_Index": index_value}