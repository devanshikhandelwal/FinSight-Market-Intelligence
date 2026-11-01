# FinSight – Financial Market Analytics Dashboard

An interactive Streamlit dashboard built from the supplied FinSight CSV datasets.

## Features
- Market overview KPIs and cumulative return comparison
- Historical cumulative performance
- Individual stock price and moving-average analysis
- Risk vs return, volatility and maximum drawdown
- Sector-level performance and distribution
- Sector, stock and date filters
- Downloadable filtered summary

## Run locally (Windows PowerShell)

1. Extract this folder into your existing FinSight project, or use it as a standalone folder.
2. Open PowerShell in this folder.
3. Create/activate a virtual environment if needed:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
4. Install packages:
   ```powershell
   pip install -r requirements.txt
   ```
5. Start the dashboard:
   ```powershell
   streamlit run app.py
   ```
6. Streamlit opens the dashboard in your browser, usually at `http://localhost:8501`.

## Data files
The three CSV files are in `data/processed/`. Keep those filenames and folder structure unchanged.

## Notes
Returns, volatility and drawdown are historical calculations from the supplied dataset. They are not forecasts or investment advice. Check source data, adjusted-price methodology and benchmark comparisons before presenting results as investment conclusions.
