
import time
import pandas as pd
import yfinance as yf

from sqlalchemy import text
from src.database.db import engine


# ==========================================
# FINSIGHT - STOCK DATA COLLECTION
# ==========================================

STOCKS = {
    "RELIANCE.NS": ("Reliance Industries", "Energy"),
    "TCS.NS": ("TCS", "IT"),
    "HDFCBANK.NS": ("HDFC Bank", "Banking"),
    "ICICIBANK.NS": ("ICICI Bank", "Banking"),
    "INFY.NS": ("Infosys", "IT"),
    "ITC.NS": ("ITC", "FMCG"),
    "LT.NS": ("Larsen & Toubro", "Infrastructure"),
    "SBIN.NS": ("State Bank of India", "Banking"),
    "BHARTIARTL.NS": ("Bharti Airtel", "Telecom"),
    "AXISBANK.NS": ("Axis Bank", "Banking"),
}


def clean_number(value):
    """Convert numeric values safely."""
    if pd.isna(value):
        return None
    return float(value)


def collect_stock_data(symbol, company_name, sector):

    print(f"\nDownloading: {symbol}")

    try:
        ticker = yf.Ticker(symbol)

        df = ticker.history(
            period="5y",
            interval="1d",
            auto_adjust=False,
            actions=False
        )

        if df.empty:
            print(f"No data available for {symbol}")
            return

        df = df.reset_index()

        # Insert stock information
        with engine.begin() as connection:

            connection.execute(
                text("""
                    INSERT INTO stocks
                        (symbol, company_name, sector)
                    VALUES
                        (:symbol, :company_name, :sector)
                    ON CONFLICT (symbol)
                    DO UPDATE SET
                        company_name = EXCLUDED.company_name,
                        sector = EXCLUDED.sector
                """),
                {
                    "symbol": symbol,
                    "company_name": company_name,
                    "sector": sector
                }
            )

            stock_id = connection.execute(
                text("""
                    SELECT stock_id
                    FROM stocks
                    WHERE symbol = :symbol
                """),
                {"symbol": symbol}
            ).scalar_one()

            records = []

            for _, row in df.iterrows():

                trade_date = pd.to_datetime(row["Date"]).date()

                records.append({
                    "stock_id": stock_id,
                    "trade_date": trade_date,
                    "open": clean_number(row["Open"]),
                    "high": clean_number(row["High"]),
                    "low": clean_number(row["Low"]),
                    "close": clean_number(row["Close"]),
                    "adj_close": clean_number(
                        row["Adj Close"]
                    ) if "Adj Close" in df.columns else None,
                    "volume": (
                        int(row["Volume"])
                        if pd.notna(row["Volume"])
                        else None
                    )
                })

            connection.execute(
                text("""
                    INSERT INTO stock_prices (
                        stock_id,
                        trade_date,
                        open,
                        high,
                        low,
                        close,
                        adj_close,
                        volume
                    )
                    VALUES (
                        :stock_id,
                        :trade_date,
                        :open,
                        :high,
                        :low,
                        :close,
                        :adj_close,
                        :volume
                    )
                    ON CONFLICT (stock_id, trade_date)
                    DO UPDATE SET
                        open = EXCLUDED.open,
                        high = EXCLUDED.high,
                        low = EXCLUDED.low,
                        close = EXCLUDED.close,
                        adj_close = EXCLUDED.adj_close,
                        volume = EXCLUDED.volume
                """),
                records
            )

        print(f"Successfully saved {len(records)} records for {symbol}")

    except Exception as error:
        print(f"Error downloading {symbol}: {error}")


def collect_nifty_index():

    print("\nDownloading NIFTY 50 index...")

    try:
        df = yf.Ticker("^NSEI").history(
            period="5y",
            interval="1d",
            auto_adjust=False
        )

        if df.empty:
            print("No NIFTY index data available")
            return

        df = df.reset_index()

        records = []

        for _, row in df.iterrows():

            records.append({
                "index_name": "NIFTY 50",
                "trade_date": pd.to_datetime(row["Date"]).date(),
                "open": clean_number(row["Open"]),
                "high": clean_number(row["High"]),
                "low": clean_number(row["Low"]),
                "close": clean_number(row["Close"]),
                "volume": (
                    int(row["Volume"])
                    if pd.notna(row["Volume"])
                    else None
                )
            })

        with engine.begin() as connection:

            connection.execute(
                text("""
                    INSERT INTO market_indices (
                        index_name,
                        trade_date,
                        open,
                        high,
                        low,
                        close,
                        volume
                    )
                    VALUES (
                        :index_name,
                        :trade_date,
                        :open,
                        :high,
                        :low,
                        :close,
                        :volume
                    )
                    ON CONFLICT (index_name, trade_date)
                    DO UPDATE SET
                        open = EXCLUDED.open,
                        high = EXCLUDED.high,
                        low = EXCLUDED.low,
                        close = EXCLUDED.close,
                        volume = EXCLUDED.volume
                """),
                records
            )

        print(f"NIFTY 50: Saved {len(records)} records")

    except Exception as error:
        print(f"NIFTY download error: {error}")


if __name__ == "__main__":

    print("=" * 50)
    print("FINSIGHT STOCK MARKET DATA COLLECTION")
    print("=" * 50)

    for symbol, details in STOCKS.items():

        company_name, sector = details

        collect_stock_data(
            symbol,
            company_name,
            sector
        )

        time.sleep(1)

    collect_nifty_index()

    print("\n" + "=" * 50)
    print("DATA COLLECTION PROCESS COMPLETED")
    print("=" * 50)
