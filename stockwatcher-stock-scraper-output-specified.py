# Usage: python3 stockwatcher-stock-scraper.py <stock_ticker> <folder_path> <start_date> [<end_date>]

import sys
import os
import yfinance as yf
import pandas as pd
from datetime import datetime

# Function to scrape and save data to a CSV file
def scrape_and_save_data(ticker, folder_path, start_date, end_date=None):
    # Set the end date to today if not specified
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')

    # Fetch data from Yahoo Finance
    data = yf.download(ticker, start=start_date, end=end_date)

    # Select and reorder columns
    data = data[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]

    # Rename columns
    data.columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

    # Define the file path and name based on ticker, start_date, and end_date
    file_name = os.path.join(folder_path, f"{ticker}_from_{start_date}_to_{end_date}.csv")

    # Save data to a CSV file
    data.to_csv(file_name, date_format='%Y-%m-%d')

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 script.py <ticker> <folder_path> <start_date> [<end_date>]")
        sys.exit(1)

    ticker = sys.argv[1]
    folder_path = sys.argv[2]
    start_date = sys.argv[3]

    if len(sys.argv) > 4:
        end_date = sys.argv[4]
    else:
        end_date = None

    # Create the output folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Disable yfinance logs if needed
    yf.pdr_override()

    # Call the function to scrape and save data
    scrape_and_save_data(ticker, folder_path, start_date, end_date)
