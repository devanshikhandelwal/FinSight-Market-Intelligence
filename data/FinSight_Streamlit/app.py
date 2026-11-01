from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="FinSight | Market Intelligence", page_icon="📈", layout="wide")

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "processed"

@st.cache_data
def load_data():
    daily = pd.read_csv(DATA / "daily_stock_metrics.csv", parse_dates=["trade_date"])
    summary = pd.read_csv(DATA / "stock_performance_summary.csv", parse_dates=["first_date", "last_date"])
    periodic = pd.read_csv(DATA / "periodic_returns.csv", parse_dates=["period"])
    return daily, summary, periodic

daily, summary, periodic = load_data()

# FinTech styling
st.markdown("""
<style>
.stApp { background: #071525; color: #EAF2FA; }
[data-testid="stSidebar"] { background: #0D2034; }
.block-container { padding-top: 1.5rem; max-width: 1500px; }
h1,h2,h3,p,label { color: #EAF2FA; }
[data-testid="stMetric"] { background: linear-gradient(135deg,#102B45,#123A4B); border: 1px solid #24516A; padding: 16px; border-radius: 14px; }
[data-testid="stMetricLabel"] { color: #A9C2D6; }
[data-testid="stMetricValue"] { color: #FFFFFF; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>📈 FINSIGHT</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#8FB4C9;font-size:16px'>INDIAN EQUITY MARKET · PERFORMANCE · RISK · SECTOR INTELLIGENCE</p>", unsafe_allow_html=True)
st.divider()

# Sidebar filters
st.sidebar.title("Dashboard Filters")
sectors = sorted(summary["sector"].dropna().unique().tolist())
chosen_sectors = st.sidebar.multiselect("Sector", sectors, default=sectors)
filtered_summary = summary[summary["sector"].isin(chosen_sectors)].copy()
symbols = sorted(filtered_summary["symbol"].unique().tolist())
chosen_symbols = st.sidebar.multiselect("Stocks", symbols, default=symbols)
filtered_summary = filtered_summary[filtered_summary["symbol"].isin(chosen_symbols)]
min_date = daily["trade_date"].min().date()
max_date = daily["trade_date"].max().date()
date_range = st.sidebar.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered_daily = daily[
    daily["symbol"].isin(chosen_symbols)
    & daily["sector"].isin(chosen_sectors)
    & daily["trade_date"].dt.date.between(start_date, end_date)
].copy()
filtered_periodic = periodic[
    periodic["symbol"].isin(chosen_symbols)
    & periodic["period"].dt.date.between(start_date, end_date)
].copy()

if filtered_summary.empty:
    st.warning("No stocks match the selected filters. Please change the filters.")
    st.stop()

# KPIs
avg_return = filtered_summary["cumulative_return"].mean()
avg_vol = filtered_summary["annualized_volatility"].mean()
worst_dd = filtered_summary["maximum_drawdown"].min()
best = filtered_summary.loc[filtered_summary["cumulative_return"].idxmax()]
c1,c2,c3,c4 = st.columns(4)
c1.metric("Stocks analysed", f"{filtered_summary['symbol'].nunique():,}")
c2.metric("Average cumulative return", f"{avg_return:.2%}")
c3.metric("Average annualized volatility", f"{avg_vol:.2%}")
c4.metric("Worst maximum drawdown", f"{worst_dd:.2%}")
st.caption(f"Best performer in current selection: **{best['company_name']}** ({best['cumulative_return']:.2%}) · Data: {start_date} to {end_date}")
st.divider()

overview, stock_tab, risk_tab, sector_tab, data_tab = st.tabs(
    ["Market Overview", "Stock Analysis", "Risk Analytics", "Sector Analysis", "Data"]
)

template = "plotly_dark"
chart_bg = "#0D2034"
paper_bg = "#0D2034"

with overview:
    left, right = st.columns([1.05,1.4])
    with left:
        perf = filtered_summary.sort_values("cumulative_return", ascending=True)
        fig = px.bar(perf, x="cumulative_return", y="symbol", orientation="h",
                     color="cumulative_return", color_continuous_scale=["#EF6461","#F4B860","#19C6A7"],
                     hover_data=["company_name","sector"], title="Cumulative return by stock")
        fig.update_layout(template=template, paper_bgcolor=paper_bg, plot_bgcolor=chart_bg,
                          xaxis_tickformat=".0%", coloraxis_showscale=False, height=440,
                          margin=dict(l=10,r=10,t=55,b=10))
        st.plotly_chart(fig, use_container_width=True)
    with right:
        trend = filtered_daily.sort_values("trade_date")
        fig = px.line(trend, x="trade_date", y="cumulative_return", color="symbol",
                      hover_data=["company_name"], title="Historical cumulative performance")
        fig.update_layout(template=template, paper_bgcolor=paper_bg, plot_bgcolor=chart_bg,
                          yaxis_tickformat=".0%", height=440, margin=dict(l=10,r=10,t=55,b=10),
                          legend_title_text="Stock")
        st.plotly_chart(fig, use_container_width=True)
    st.subheader("Performance snapshot")
    show = filtered_summary[["symbol","company_name","sector","cumulative_return","annualized_volatility","maximum_drawdown","trading_days"]].copy()
    for col in ["cumulative_return","annualized_volatility","maximum_drawdown"]:
        show[col] = show[col].map(lambda x: f"{x:.2%}")
    st.dataframe(show.sort_values("company_name"), use_container_width=True, hide_index=True)

with stock_tab:
    stock_options = filtered_summary["symbol"].tolist()
    selected = st.selectbox("Choose a stock", stock_options, format_func=lambda s: filtered_summary.loc[filtered_summary.symbol.eq(s),"company_name"].iloc[0])
    one = filtered_daily[filtered_daily["symbol"] == selected].sort_values("trade_date")
    if one.empty:
        st.info("No daily observations for this stock in the selected date range.")
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=one.trade_date, y=one.analysis_price, name="Analysis price", line=dict(color="#19C6A7",width=2)))
        if one["SMA_20"].notna().any():
            fig.add_trace(go.Scatter(x=one.trade_date, y=one.SMA_20, name="20-day SMA", line=dict(color="#F4B860",width=1.5)))
        if one["SMA_50"].notna().any():
            fig.add_trace(go.Scatter(x=one.trade_date, y=one.SMA_50, name="50-day SMA", line=dict(color="#8C7CFF",width=1.5)))
        fig.update_layout(title="Price and moving averages", template=template, paper_bgcolor=paper_bg,
                          plot_bgcolor=chart_bg, height=430)
        st.plotly_chart(fig, use_container_width=True)
        vol_fig = px.bar(one, x="trade_date", y="volume", title="Daily trading volume")
        vol_fig.update_layout(template=template, paper_bgcolor=paper_bg, plot_bgcolor=chart_bg, height=300)
        st.plotly_chart(vol_fig, use_container_width=True)

with risk_tab:
    left,right = st.columns(2)
    with left:
        fig = px.scatter(filtered_summary, x="annualized_volatility", y="cumulative_return",
                         size="trading_days", color="sector", hover_name="company_name",
                         text="symbol", title="Risk vs return")
        fig.update_traces(textposition="top center")
        fig.update_layout(template=template, paper_bgcolor=paper_bg, plot_bgcolor=chart_bg,
                          xaxis_tickformat=".0%", yaxis_tickformat=".0%", height=430)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        risk = filtered_summary.sort_values("maximum_drawdown")
        fig = px.bar(risk, x="maximum_drawdown", y="symbol", orientation="h",
                     color="maximum_drawdown", color_continuous_scale=["#EF6461","#F4B860","#19C6A7"],
                     title="Maximum drawdown by stock")
        fig.update_layout(template=template, paper_bgcolor=paper_bg, plot_bgcolor=chart_bg,
                          xaxis_tickformat=".0%", coloraxis_showscale=False, height=430)
        st.plotly_chart(fig, use_container_width=True)
    fig = px.bar(filtered_summary.sort_values("annualized_volatility",ascending=False),
                 x="symbol", y="annualized_volatility", color="sector",
                 title="Annualized volatility by stock")
    fig.update_layout(template=template, paper_bgcolor=paper_bg, plot_bgcolor=chart_bg,
                      yaxis_tickformat=".0%", height=350)
    st.plotly_chart(fig, use_container_width=True)

with sector_tab:
    sector_perf = filtered_summary.groupby("sector", as_index=False).agg(
        average_return=("cumulative_return","mean"),
        average_volatility=("annualized_volatility","mean"),
        stocks=("symbol","nunique"))
    left,right = st.columns(2)
    with left:
        fig = px.bar(sector_perf.sort_values("average_return"), x="average_return", y="sector",
                     orientation="h", color="average_return",
                     color_continuous_scale=["#EF6461","#F4B860","#19C6A7"],
                     title="Average cumulative return by sector")
        fig.update_layout(template=template, paper_bgcolor=paper_bg, plot_bgcolor=chart_bg,
                          xaxis_tickformat=".0%", coloraxis_showscale=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig = px.pie(sector_perf, names="sector", values="stocks", hole=.58,
                     title="Stock distribution by sector")
        fig.update_layout(template=template, paper_bgcolor=paper_bg, height=400)
        st.plotly_chart(fig, use_container_width=True)
    fig = px.bar(sector_perf, x="sector", y="average_volatility", color="average_volatility",
                 title="Average annualized volatility by sector")
    fig.update_layout(template=template, paper_bgcolor=paper_bg, plot_bgcolor=chart_bg,
                      yaxis_tickformat=".0%", coloraxis_showscale=False, height=330)
    st.plotly_chart(fig, use_container_width=True)

with data_tab:
    st.subheader("Stock performance summary")
    st.dataframe(filtered_summary, use_container_width=True, hide_index=True)
    st.subheader("Daily metrics")
    st.dataframe(filtered_daily.head(500), use_container_width=True, hide_index=True)
    st.download_button("Download filtered summary CSV",
                       filtered_summary.to_csv(index=False).encode("utf-8"),
                       "finsight_filtered_summary.csv", "text/csv")

st.markdown("<hr><p style='color:#7896AA;text-align:center'>FinSight · Educational analytics project · Historical data, not investment advice</p>", unsafe_allow_html=True)
