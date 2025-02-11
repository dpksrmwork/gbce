import sqlite3
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.src.models.stock import Stock
from app.src.models.trade import Trade

DB_PATH = "gbc_exchange.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create stocks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            symbol TEXT PRIMARY KEY,
            stock_type TEXT NOT NULL,
            last_dividend REAL NOT NULL,
            par_value REAL NOT NULL,
            fixed_dividend REAL
        )
    """)

    # Create trades table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
        id TEXT PRIMARY KEY, 
        timestamp TEXT NOT NULL,
        stock_symbol TEXT NOT NULL,    
        quantity INTEGER NOT NULL CHECK (quantity > 0),
        trade_type TEXT NOT NULL CHECK (trade_type IN ('buy', 'sell')),
        price REAL NOT NULL CHECK (price > 0),
        FOREIGN KEY(stock_symbol) REFERENCES stocks(symbol)
    )
    """)

    conn.commit()
    conn.close()


def get_db_connection():
    """Establish and return a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


# Add a new stock
def add_stock(stock: Stock):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO stocks (symbol, stock_type, last_dividend, par_value, fixed_dividend)
            VALUES (?, ?, ?, ?, ?)
        """, (stock.symbol, stock.stock_type, stock.last_dividend, stock.par_value, stock.fixed_dividend))
        conn.commit()
    except sqlite3.IntegrityError:
        return {"error": "Stock already exists with the given symbol"}
    finally:
        conn.close()
    return {"message": "Stock added successfully"}


# Get stock by symbol
def get_stock(symbol: str) -> Stock | None:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM stocks WHERE symbol = ?", (symbol,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return Stock(symbol=row[0], stock_type=row[1], last_dividend=row[2], par_value=row[3], fixed_dividend=row[4])
    return None

# Add a trade
def add_trade(trade: Trade):

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if stock exists
    cursor.execute("SELECT * FROM stocks WHERE symbol = ?", (trade.stock_symbol,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Stock does not exist.")

    # Insert trade
    cursor.execute(
        "INSERT INTO trades (id, stock_symbol, timestamp, quantity, trade_type, price) VALUES (?, ?, ?, ?, ?, ?)",
        (trade.id, trade.stock_symbol, trade.timestamp, trade.quantity, trade.trade_type, trade.price)
    )

    conn.commit()
    conn.close()

def get_trades_for_stock(symbol: str, minutes: int = None):
    """
    Fetch trades for a given stock.
    
    :param symbol: Stock symbol
    :param minutes: Optional time period in minutes. If None, fetch all trades.
    :return: List of Trade objects
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    if minutes:
        time_threshold = datetime.utcnow() - timedelta(minutes=minutes)
        cursor.execute(
            "SELECT * FROM trades WHERE stock_symbol = ? AND timestamp >= ?",
            (symbol, time_threshold.isoformat()),
        )
    else:
        cursor.execute("SELECT * FROM trades WHERE stock_symbol = ?", (symbol,))
    
    trades = [Trade(**dict(row)) for row in cursor.fetchall()]
    conn.close()
    
    return trades


def get_all_stocks() -> list[Stock]:
    """
    Fetch all stocks from the database and return them as Pydantic Stock models.
    
    :return: A list of Stock objects.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT symbol, stock_type, last_dividend, fixed_dividend, par_value FROM stocks")
    stocks = cursor.fetchall()
    
    conn.close()
    
    return [
        Stock(
            symbol=row[0],
            stock_type=row[1],
            last_dividend=row[2],
            fixed_dividend=row[3],
            par_value=row[4]
        )
        for row in stocks
    ]
