import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import time
import os
import warnings

# --- STYLE & CONFIG ---
warnings.filterwarnings("ignore")
pd.options.display.max_columns = None
pd.options.display.width = 1000
pd.options.display.precision = 2  # Fixed the broken line here

def gold_complete_analytics_system():
    file_path = "gold_master_database.csv"
    tax_factor = 1.092  # 6% Import Duty + 3% GST
    
    print("\n")
    print(" GOLD PREMIER ANALYTICS")
    print("═"*80)
    
    # Removed 'while True' to prevent the code from repeating every 60 seconds
    try:
        # 1. DATA ACQUISITION
        gold_h = yf.download("GC=F", period="2y", interval="1d", progress=False)
        inr_h = yf.download("INR=X", period="2y", interval="1d", progress=False)
        
        if isinstance(gold_h.columns, pd.MultiIndex): gold_h.columns = gold_h.columns.get_level_values(0)
        if isinstance(inr_h.columns, pd.MultiIndex): inr_h.columns = inr_h.columns.get_level_values(0)

        df = pd.merge(gold_h[['Close']], inr_h[['Close']].rename(columns={'Close':'USDINR'}), 
                     left_index=True, right_index=True).dropna()
        
        df['Price_Gram'] = (df['Close'] / 31.1034768) * df['USDINR'] * tax_factor

        # 2. DATA REPRESENTATION
        print("\n [1] SYSTEM INfO ")
        df.info()

        print("\n [2] DATASET INSPECTION ")
        print(df[['Price_Gram', 'USDINR']].tail(5))
        
        # 3.descibing the data
        print("\n [3] SYSTEM DATA ")
        print(df.describe())
        
        # 4.HEAD
        df.head()
       
        # 5. DATA CLEANING & QUALITY CHECK
        print("\n [4] DATA CLEANING " )
        initial_count = len(df)
        
        # Handling Missing Values
        missing_count = df.isnull().sum().sum()
        df = df.dropna()
        

        # 6. FORECAST ENGINE
        df_m = df.reset_index()
        df_m['Ordinal'] = df_m['Date'].map(pd.Timestamp.toordinal)
        
        bullish_data = df_m.tail(120)
        model_bullish = LinearRegression().fit(bullish_data[['Ordinal']], bullish_data['Price_Gram'])
        model_stable = LinearRegression().fit(df_m[['Ordinal']], df_m['Price_Gram'])
        
        future_months = pd.date_range(start="2026-01-01", end="2026-12-01", freq='MS')
        future_ord = np.array([d.toordinal() for d in future_months]).reshape(-1, 1)
        
        preds_bullish = model_bullish.predict(future_ord)
        preds_stable = model_stable.predict(future_ord)

        # 7. TEXT FORECAST REPORT
        print("\n" + "@" * 3 + " 2026 BULLISH HIGH FORECAST REPORT " + "@" * 3)
        report = pd.DataFrame({
            'Month': future_months.strftime('%B %Y'),
            'Stable Est (₹)': preds_stable,
            'BULLISH HIGH (₹)': preds_bullish
        })
        print(report.to_string(index=False))

        # 5. VISUALIZATION
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        ax1.plot(df.index[-180:], df['Price_Gram'].tail(180), label='Historical')
        ax1.plot(future_months, preds_bullish, marker='o', label='2026 Forecast')
        ax1.set_title("Gold Price Projection")
        ax1.legend()

        corr_data = bullish_data[['Close', 'USDINR', 'Price_Gram']].corr()
        sns.heatmap(corr_data, annot=True, cmap='YlOrRd', ax=ax2)
        
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f" Error occurred: {e}")

if __name__ == "__main__":
    gold_complete_analytics_system()
analyse this code give me the description of these
