
import pandas as pd
import numpy as np
from sqlalchemy import text

from src.database.db import engine


# ==========================================
# FINSIGHT - FINANCIAL DATA ANALYSIS
# ==========================================

def load_stock_data():

    query = """
        SELECT
            s.symbol,
            s.company_name,
            s.sector,
            sp.trade_date,
            sp.close,
            sp.adj_close,
            sp.volume
        FROM stock_prices sp
        JOIN stocks s
            ON sp.stock_id = s.stock_id
        ORDER BY s.symbol, sp.trade_date
    """

    with engine.connect() as connection:
        df = pd.read_sql(text(query), connection)

    if df.empty:
        raise ValueError(
            "No stock data found. Check your PostgreSQL tables."
        )

    df["trade_date"] = pd.to_datetime(df["trade_date"])

    return df


def calculate_daily_metrics(df):

    df = df.copy()

    # Use adjusted closing price where available.
    # Otherwise, use regular closing price.
    df["analysis_price"] = (
        df["adj_close"].fillna(df["close"])
    )

    df = df.sort_values(
        ["symbol", "trade_date"]
    )

    grouped = df.groupby("symbol")["analysis_price"]

    # Daily returns
    df["daily_return"] = grouped.pct_change(
        fill_method=None
    )

    # Moving averages
    df["SMA_20"] = grouped.transform(
        lambda x: x.rolling(20).mean()
    )

    df["SMA_50"] = grouped.transform(
        lambda x: x.rolling(50).mean()
    )

    # Annualized rolling volatility
    df["volatility_20d"] = (
        df.groupby("symbol")["daily_return"]
        .transform(
            lambda x: x.rolling(20).std() * np.sqrt(252)
        )
    )

    # Cumulative returns
    df["cumulative_return"] = (
        df.groupby("symbol")["analysis_price"]
        .transform(lambda x: x / x.iloc[0] - 1)
    )

    # Drawdown
    df["running_peak"] = (
        df.groupby("symbol")["analysis_price"]
        .cummax()
    )

    df["drawdown"] = (
        df["analysis_price"] / df["running_peak"] - 1
    )

    return df


def calculate_periodic_returns(df):

    results = []

    for symbol, group in df.groupby("symbol"):

        group = group.sort_values("trade_date")

        prices = (
            group.set_index("trade_date")
            ["analysis_price"]
        )

        # Weekly closing prices
        weekly_prices = prices.resample("W-FRI").last().dropna()

        weekly_returns = weekly_prices.pct_change(
            fill_method=None
        )

        for date, value in weekly_returns.items():
            results.append({
                "symbol": symbol,
                "period": date,
                "period_type": "Weekly",
                "return": value
            })

        # Month-end closing prices
        monthly_prices = prices.resample("ME").last().dropna()

        monthly_returns = monthly_prices.pct_change(
            fill_method=None
        )

        for date, value in monthly_returns.items():
            results.append({
                "symbol": symbol,
                "period": date,
                "period_type": "Monthly",
                "return": value
            })

    return pd.DataFrame(results)


def calculate_stock_summary(df):

    summary = []

    for symbol, group in df.groupby("symbol"):

        group = group.sort_values("trade_date")

        valid_returns = group["daily_return"].dropna()

        annual_volatility = (
            valid_returns.std() * np.sqrt(252)
            if len(valid_returns) > 1
            else np.nan
        )

        max_drawdown = group["drawdown"].min()

        cumulative_return = (
            group["analysis_price"].iloc[-1]
            / group["analysis_price"].iloc[0] - 1
        )

        summary.append({
            "symbol": symbol,
            "company_name": group["company_name"].iloc[0],
            "sector": group["sector"].iloc[0],
            "first_date": group["trade_date"].min(),
            "last_date": group["trade_date"].max(),
            "trading_days": len(group),
            "cumulative_return": cumulative_return,
            "annualized_volatility": annual_volatility,
            "maximum_drawdown": max_drawdown
        })

    return pd.DataFrame(summary)


def main():

    print("=" * 50)
    print("FINSIGHT FINANCIAL ANALYTICS")
    print("=" * 50)

    print("\nLoading data from PostgreSQL...")

    df = load_stock_data()

    print("Records loaded:", len(df))
    print("Stocks found:", df["symbol"].nunique())

    print("\nCalculating daily financial metrics...")

    daily_df = calculate_daily_metrics(df)

    print("\nCalculating weekly and monthly returns...")

    periodic_df = calculate_periodic_returns(daily_df)

    print("\nGenerating stock performance summary...")

    summary_df = calculate_stock_summary(daily_df)

    # Save analytical datasets
    daily_df.to_csv(
        "data/processed/daily_stock_metrics.csv",
        index=False
    )

    periodic_df.to_csv(
        "data/processed/periodic_returns.csv",
        index=False
    )

    summary_df.to_csv(
        "data/processed/stock_performance_summary.csv",
        index=False
    )

    print("\nTOP STOCK PERFORMERS")

    print(
        summary_df.sort_values(
            "cumulative_return",
            ascending=False
        ).to_string(index=False)
    )

    print("\nAll analytical datasets saved successfully!")

    print("\nFINSIGHT FINANCIAL ANALYSIS COMPLETED!")


if __name__ == "__main__":
    main()
