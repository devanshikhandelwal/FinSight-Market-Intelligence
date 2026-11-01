# FinSight – Market Intelligence Dashboard

An interactive Indian stock market analytics platform built using Python, PostgreSQL, Pandas, Plotly and Streamlit.

## Overview

FinSight is a financial data analytics project designed to analyze historical stock market performance, compare stocks, evaluate investment risk and visualize financial trends through an interactive dashboard.

The project combines data collection, data processing, financial analysis, database management and interactive visualization.

## Key Features

- **Market Overview:** Compare cumulative returns and historical stock performance.
- **Stock Analysis:** Explore stock prices, moving averages (SMA 20 and SMA 50), and trading volume.
- **Risk Analytics:** Evaluate annualized volatility, maximum drawdown and risk-return relationships.
- **Sector Analysis:** Compare average returns and volatility across sectors.
- **Interactive Filters:** Filter dashboard results by stock, sector and date range.
- **Data Exploration:** View analytical datasets and download filtered summaries.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming and analysis |
| Pandas | Data manipulation |
| PostgreSQL | Database management |
| Plotly | Interactive visualizations |
| Streamlit | Dashboard development |
| Git & GitHub | Version control |

## Project Structure

```text
FinSight/
│
├── data/
│   ├── processed/
│   └── FinSight_Streamlit/
│       ├── app.py
│       ├── requirements.txt
│       └── data/
│           └── processed/
│
├── reports/
│   ├── historical_returns.html
│   ├── risk_return.html
│   ├── sector_performance.html
│   └── stock_performance.html
│
├── src/
│   ├── analytics/
│   ├── config/
│   ├── database/
│   └── ingestion/
│
├── .gitignore
└── requirements.txt
```

## How to Run the Dashboard

### 1. Clone the repository

```bash
git clone https://github.com/devanshikhandelwal/FinSight-Market-Intelligence.git
```

### 2. Navigate to the dashboard folder

```bash
cd FinSight-Market-Intelligence/data/FinSight_Streamlit
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Launch the dashboard

```bash
streamlit run app.py
```

The dashboard will open locally in your browser, usually at:

`http://localhost:8501`
## 🚀 Live Demo

**Explore FinSight – Market Intelligence:** 

[![Live Dashboard](https://img.shields.io/badge/Streamlit-Live%20Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://finsight-market-intelligence-42mxv7kdds5hhyqhgzcwzq.streamlit.app/)

👉 [**Launch FinSight Dashboard**](https://finsight-market-intelligence-42mxv7kdds5hhyqhgzcwzq.streamlit.app/)

Explore interactive stock market analytics, performance comparisons, risk metrics, and sector-level insights.

## Data and Analysis

FinSight uses processed historical stock market datasets to calculate and visualize:

- Periodic stock returns
- Cumulative returns
- Moving averages
- Annualized volatility
- Maximum drawdown
- Historical performance metrics

## Future Enhancements

- Deploy the dashboard online.
- Integrate automated stock market data updates.
- Add portfolio tracking and comparison.
- Introduce additional financial indicators.
- Add more advanced analytical insights.

## Disclaimer

FinSight is an educational data analytics project. Its visualizations and metrics are intended for learning and research purposes and should not be considered financial advice or investment recommendations.

## Author

**Devanshi Khandelwal**

GitHub: https://github.com/devanshikhandelwal
