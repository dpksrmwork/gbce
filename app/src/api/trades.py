from fastapi import APIRouter
from app.src.models.trade import Trade
from app.src.services.gbc_db import add_trade
from app.src.utils.audit_helper import generate_transaction_id

router = APIRouter()

@router.post("/")
def create_trade(trade: Trade):
    transaction_id = generate_transaction_id()
    add_trade(trade)
    return {
        "transaction_id": transaction_id,
        "message": "Trade recorded successfully",
        "stock_symbol": trade.stock_symbol,
        "price": trade.price
        }
