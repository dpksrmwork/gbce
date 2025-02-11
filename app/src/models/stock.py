from pydantic import BaseModel, Field, model_validator
from typing import Optional
from enum import Enum


class StockType(str, Enum):
    """Enum representing stock types: Common or Preferred"""
    COMMON = "Common"
    PREFERRED = "Preferred"


class Stock(BaseModel):
    """Represents a stock with relevant financial details"""

    symbol: str = Field(..., description="Unique identifier for the stock")
    stock_type: StockType = Field(..., description="Type of stock (Common or Preferred)")
    last_dividend: Optional[float] = Field(None, description="Last dividend paid by the stock")
    par_value: float = Field(..., gt=0, description="Par value of the stock. Must be greater than zero.")
    fixed_dividend: Optional[float] = Field(None, description="Fixed dividend percentage (for Preferred stocks)")

    @model_validator(mode="before")
    @classmethod
    def normalize_stock_type(cls, values):
        """
        Ensures stock_type is case insensitive.
        Converts any variation of 'common' or 'preferred' to proper enum values.
        """
        stock_type = values.get("stock_type")

        if isinstance(stock_type, str):
            normalized_type = stock_type.capitalize()  # Converts "common", "COMMON" to "Common"
            if normalized_type not in StockType.__members__.values():
                raise ValueError("Invalid stock type. Must be 'Common' or 'Preferred'.")
            values["stock_type"] = StockType(normalized_type)

        return values

    @model_validator(mode="before")
    @classmethod
    def check_dividends(cls, values):
        """
        Ensures at least one of last_dividend or fixed_dividend is provided.
        """
        last_dividend = values.get("last_dividend")
        fixed_dividend = values.get("fixed_dividend")

        if last_dividend is None and fixed_dividend is None:
            raise ValueError("Either 'last_dividend' or 'fixed_dividend' must be provided.")

        return values
