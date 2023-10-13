# run $ python3 stockwatcher-scrape.py <ticker> </path/to/output_folder> <YYYY-MM-DD> [<YYYY-MM-DD>]
# or run $ python3 stockwatcher-scrape.py </path/to/ticker/list.txt> </path/to/output_folder> <YYYY-MM-DD> [<YYYY-MM-DD>]
# ticker must be separated by commas in the ticker list txt file
# don't forget to pip install -r ./requirements.txt

import yfinance as yf
import os
import sys
import csv

# Function to download data for a single stock
def download_stock_data(ticker, start_date, end_date, output_folder):
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if not data.empty:
            output_file = os.path.join(output_folder, f"{ticker}_from_{start_date}_to_{end_date}.csv")
            data.to_csv(output_file)
            print(f"Downloaded data for {ticker} to {output_file}")
        else:
            print(f"No data available for {ticker}")
    except Exception as e:
        print(f"Failed to download data for {ticker}: {str(e)}")

# Main function to handle command-line arguments
def main():
    if len(sys.argv) < 4:
        print("Usage: python3 script.py <ticker/ticker_list_path> <output_folder_path> <start_date> [end_date]")
        return

    ticker_input = sys.argv[1]
    output_folder = sys.argv[2]
    start_date = sys.argv[3]
    end_date = None if len(sys.argv) < 5 else sys.argv[4]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    tickers = []
    if os.path.isfile(ticker_input) and ticker_input.endswith(".txt"):
        with open(ticker_input, 'r') as file:
            tickers = [line.strip() for line in file.read().split(',')]
    else:
        tickers = ticker_input.split(',')

    for ticker in tickers:
        download_stock_data(ticker, start_date, end_date, output_folder)

if __name__ == "__main__":
    main()
