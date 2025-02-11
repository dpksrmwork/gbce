from enum import Enum
from uuid import uuid4
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class TradeType(str, Enum):
    """Enum representing trade types: Buy or Sell"""
    BUY = "buy"
    SELL = "sell"


class Trade(BaseModel):
    """Represents a stock trade transaction"""

    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier for the trade (UUID).")
    stock_symbol: str = Field(..., min_length=1, max_length=10, description="Stock symbol associated with the trade.")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="Trade timestamp in ISO format")
    quantity: int = Field(..., gt=0, description="Number of shares traded. Must be greater than zero.")
    trade_type: TradeType = Field(..., description="Type of trade: 'buy' or 'sell' (case insensitive).")
    price: float = Field(..., gt=0, description="Price per share. Must be greater than zero.")

    @field_validator("stock_symbol", mode="before")
    @classmethod
    def validate_stock_symbol(cls, v: str) -> str:
        """
        Ensure stock symbol is uppercase.
        """
        return v.upper()

    @field_validator("trade_type", mode="before")
    @classmethod
    def normalize_trade_type(cls, v: str) -> str:
        """
        Converts trade_type to lowercase ('buy' or 'sell') to ensure case insensitivity.
        """
        v_lower = v.lower()
        if v_lower not in {"buy", "sell"}:
            raise ValueError("Invalid trade type. Must be 'buy' or 'sell'.")
        return v_lower

    @field_validator("timestamp", mode="before")
    @classmethod
    def parse_timestamp(cls, v: Optional[str]) -> str:
        """
        Converts different date-time formats into a standard ISO 8601 format.
        If no timestamp is provided, use the current UTC time.
        Accepts:
        - `YYYY-MM-DDTHH:MM:SS`
        - `YYYY-MM-DDTHH:MM`
        - `YYYY-MM-DD`
        """
        if v is None:
            return datetime.utcnow().isoformat()  # Use current UTC timestamp

        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v).isoformat()  # Full ISO format
            except ValueError:
                pass

            try:
                return datetime.strptime(v, "%Y-%m-%d").isoformat()  # Date only
            except ValueError:
                pass

        raise ValueError("Invalid timestamp format. Use 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM'.")
