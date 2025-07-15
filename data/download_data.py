import yfinance as yf
import pandas as pd
import os

def download_xau_usd_data(start_date="2022-01-01", end_date="2024-01-01"):
    """
    Download XAU/USD data and save to CSV
    """
    # Create data directory if it doesn't exist
    os.makedirs('./data', exist_ok=True)
    
    try:
        # Download the data for XAU/USD
        data = yf.download("GC=F", start=start_date, end=end_date, interval="1d")
        
        # Save as CSV file
        data.to_csv('./data/xau_usd_data.csv')
        print(f"Data downloaded successfully: {len(data)} rows")
        return data
        
    except Exception as e:
        print(f"Error downloading data: {e}")
        return None

if __name__ == "__main__":
    download_xau_usd_data()