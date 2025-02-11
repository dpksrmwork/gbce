import math
from datetime import datetime, timedelta
from app.src.models.stock import Stock
from app.src.models.trade import Trade
from app.src.services.gbc_db import get_trades_for_stock, get_all_stocks


def calculate_dividend_yield(stock: Stock, price: float) -> float:
    """
    Calculate the dividend yield for a given stock and price.
    - For common stocks: Last Dividend / Price
    - For preferred stocks: (Fixed Dividend * Par Value) / Price
    """
    if price <= 0:
        raise ValueError("Price must be greater than zero")

    if stock.stock_type == "Preferred" and stock.fixed_dividend is not None:
        return (stock.fixed_dividend * stock.par_value) / price
    
    return stock.last_dividend / price


def calculate_pe_ratio(stock: Stock, price: float) -> float:
    """
    Calculate the P/E Ratio for a given stock and price.
    - P/E Ratio = Price / Dividend
    - If dividend is zero, return None (instead of float('inf')) as P/E is undefined.
    """
    if price <= 0:
        raise ValueError("Price must be greater than zero")

    if stock.last_dividend == 0:
        return None  # Return None instead of infinity to avoid unrealistic values.
    
    return price / stock.last_dividend if stock.last_dividend else None


def volume_weighted_stock_price(trades: list[Trade], last_minutes: int = 5) -> float:
    """
    Calculate the Volume Weighted Stock Price based on trades in the last X minutes.
    - VWSP = (Sum of (Price * Quantity)) / (Sum of Quantities)
    """

    now = datetime.utcnow()
    time_threshold = now - timedelta(minutes=last_minutes)

    filtered_trades = [
        trade for trade in trades 
        if datetime.fromisoformat(trade.timestamp) >= time_threshold
    ]

    total_trade_value = sum(trade.price * trade.quantity for trade in filtered_trades)
    total_quantity = sum(trade.quantity for trade in filtered_trades)

    return total_trade_value / total_quantity if total_quantity > 0 else 0


def get_vwsp_for_stock(stock_symbol: str) -> float:
    """
    Fetch the Volume Weighted Stock Price (VWSP) for a given stock.
    
    :param stock_symbol: The stock symbol provided by the user.
    :return: The calculated VWSP.
    """
    trades = get_trades_for_stock(stock_symbol)  # Fetch all trades for the stock
    return volume_weighted_stock_price(trades)


def calculate_gbce_all_share_index() -> float:
    """
    Calculate the GBCE All Share Index using the geometric mean of the VWSP for all stocks.
    """
    stocks = get_all_stocks()
    vws_prices = []

    for stock in stocks:
        trades = get_trades_for_stock(stock.symbol)
        vwsp = volume_weighted_stock_price(trades)
        if vwsp > 0:
            vws_prices.append(vwsp)

    if not vws_prices:
        return 0

    product = math.prod(vws_prices)
    return product ** (1 / len(vws_prices))


