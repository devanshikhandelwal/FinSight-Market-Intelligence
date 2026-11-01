import pandas as pd
import numpy as np
import yfinance as yf
import sqlalchemy
import psycopg2
import matplotlib
import seaborn
import plotly
import sklearn

print("FinSight Environment Check")
print("-" * 35)

print("Pandas:", pd.__version__)
print("NumPy:", np.__version__)
print("Yahoo Finance: Installed")
print("SQLAlchemy: Installed")
print("PostgreSQL Driver: Installed")
print("Matplotlib: Installed")
print("Seaborn: Installed")
print("Plotly: Installed")
print("Scikit-learn: Installed")

print("-" * 35)
print("All environment checks passed!")