#Usage: python3 sctockwatcher-stock-scraper.py <stock_ticker> <start_date> [<end_date>]
#Beware, this algorithm does NOT reckon stocks of a given index. It only gives the index data.


import sys
import os
import yfinance as yf
import pandas as pd
from datetime import datetime

# Function to scrape and save data to a CSV file
def scrape_and_save_data(ticker, start_date, end_date=None, output_folder="./"):
    # Determine the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the output folder if it doesn't exist in the script directory
    output_folder_path = os.path.join(script_dir, output_folder)
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Set the end date to today if not specified
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')

    # Create a directory name based on the current date and ticker
    folder_name = f"scraped_on_{datetime.now().strftime('%H-%M-%S_%Y-%m-%d')}_{ticker}_from_{start_date}_to_{end_date}"
    folder_path = os.path.join(output_folder_path, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Fetch data from Yahoo Finance
    data = yf.download(ticker, start=start_date, end=end_date)

    # Define the file path and name
    file_name = os.path.join(folder_path, f"{ticker}_from_{start_date}_to_{end_date}.csv")

    # Select and reorder columns
    data = data[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]

    # Rename columns
    data.columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

    # Save data to a CSV file
    data.to_csv(file_name, date_format='%Y-%m-%d')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 script.py <ticker> <start_date> [<end_date>]")
        sys.exit(1)

    ticker = sys.argv[1]
    start_date = sys.argv[2]
    
    if len(sys.argv) > 3:
        end_date = sys.argv[3]
    else:
        end_date = None

    # Disable yfinance logs if needed
    yf.pdr_override()

    # Call the function to scrape and save data
    scrape_and_save_data(ticker, start_date, end_date)
