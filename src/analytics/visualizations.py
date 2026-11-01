
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# FINSIGHT - INTERACTIVE VISUALIZATIONS
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data" / "processed"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(exist_ok=True)

# Load analytical datasets
summary = pd.read_csv(
    DATA_DIR / "stock_performance_summary.csv"
)

daily = pd.read_csv(
    DATA_DIR / "daily_stock_metrics.csv"
)

daily["trade_date"] = pd.to_datetime(
    daily["trade_date"]
)

# Convert returns into percentages
summary["return_pct"] = (
    summary["cumulative_return"] * 100
)

summary["volatility_pct"] = (
    summary["annualized_volatility"] * 100
)

summary["drawdown_pct"] = (
    summary["maximum_drawdown"] * 100
)

# ==========================================
# 1. STOCK PERFORMANCE
# ==========================================

performance = summary.sort_values(
    "return_pct",
    ascending=True
)

fig1 = px.bar(
    performance,
    x="return_pct",
    y="symbol",
    orientation="h",
    color="return_pct",
    color_continuous_scale="RdYlGn",
    title="Stock Performance - Cumulative Returns",
    labels={
        "return_pct": "Cumulative Return (%)",
        "symbol": "Stock"
    },
    hover_data=["company_name", "sector"]
)

fig1.update_layout(
    template="plotly_dark",
    height=550
)

fig1.write_html(
    REPORT_DIR / "stock_performance.html"
)

# ==========================================
# 2. RISK VS RETURN ANALYSIS
# ==========================================

fig2 = px.scatter(
    summary,
    x="volatility_pct",
    y="return_pct",
    color="sector",
    size="trading_days",
    hover_name="company_name",
    text="symbol",
    title="Risk vs Return Analysis",
    labels={
        "volatility_pct": "Annualized Volatility (%)",
        "return_pct": "Cumulative Return (%)"
    }
)

fig2.update_traces(
    textposition="top center"
)

fig2.update_layout(
    template="plotly_dark",
    height=550
)

fig2.write_html(
    REPORT_DIR / "risk_return.html"
)

# ==========================================
# 3. SECTOR PERFORMANCE
# ==========================================

sector_data = (
    summary.groupby("sector", as_index=False)
    .agg(
        average_return=("return_pct", "mean"),
        stock_count=("symbol", "count")
    )
)

fig3 = px.bar(
    sector_data,
    x="sector",
    y="average_return",
    color="average_return",
    color_continuous_scale="RdYlGn",
    title="Average Sector Performance",
    labels={
        "sector": "Sector",
        "average_return": "Average Return (%)"
    }
)

fig3.update_layout(
    template="plotly_dark",
    height=500
)

fig3.write_html(
    REPORT_DIR / "sector_performance.html"
)

# ==========================================
# 4. HISTORICAL STOCK PRICE TRENDS
# ==========================================

selected_stocks = [
    "BHARTIARTL.NS",
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS"
]

chart_data = daily[
    daily["symbol"].isin(selected_stocks)
].copy()

fig4 = px.line(
    chart_data,
    x="trade_date",
    y="cumulative_return",
    color="symbol",
    title="Historical Cumulative Stock Returns",
    labels={
        "trade_date": "Date",
        "cumulative_return": "Cumulative Return",
        "symbol": "Stock"
    }
)

fig4.update_layout(
    template="plotly_dark",
    height=550
)

fig4.write_html(
    REPORT_DIR / "historical_returns.html"
)

print("=" * 45)
print("FINSIGHT VISUALIZATIONS COMPLETED")
print("=" * 45)

print("\nGenerated files:")

for file in REPORT_DIR.glob("*.html"):
    print(file.name)

print("\nOpen the HTML files in your browser.")
