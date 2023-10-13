import os
import pandas as pd
import sys
from datetime import datetime
import calendar

def process_stock_data(input_file, output_folder, period):
    try:
        # Read the input CSV file
        df = pd.read_csv(input_file)
        
        # Convert 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        if period == 'monthly':
            # Group data by month
            df['YearMonth'] = df['Date'].dt.to_period('M')
            df['Up'] = df.groupby('YearMonth')['Adj Close'].transform(lambda x: x.iat[-1] > x.iat[0])
            monthly_stats = df.groupby('YearMonth')['Up'].agg(Up='sum', Down=lambda x: len(x) - x.sum()).reset_index()
            monthly_stats['YearMonth'] = monthly_stats['YearMonth'].dt.strftime('%Y-%B')

            # Output file name
            output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(input_file))[0] + '_monthly_statistics.csv')
        elif period == 'weekly':
            # Group data by week
            df['Week'] = df['Date'].dt.strftime('%U-%Y')
            df['Up'] = df.groupby('Week')['Adj Close'].transform(lambda x: x.iat[-1] > x.iat[0])
            weekly_stats = df.groupby('Week')['Up'].agg(Up='sum', Down=lambda x: len(x) - x.sum()).reset_index()
            
            # Output file name
            output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(input_file))[0] + '_weekly_statistics.csv')
        else:
            raise ValueError("Invalid period. Please choose 'monthly' or 'weekly'.")

        # Create the output CSV file
        if period == 'monthly':
            monthly_stats.to_csv(output_file, index=False, header=['Month', 'Up', 'Down'])
        elif period == 'weekly':
            weekly_stats.to_csv(output_file, index=False, header=['Week', 'Up', 'Down'])
        
        print(f"Processed {input_file}")
    except Exception as e:
        print(f"Failed to process {input_file}: {e}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_csv_or_folder> <output_folder> <monthly/weekly>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_folder = sys.argv[2]
    period = sys.argv[3]

    if os.path.isfile(input_path):
        process_stock_data(input_path, output_folder, period)
    elif os.path.isdir(input_path):
        for file in os.listdir(input_path):
            file_path = os.path.join(input_path, file)
            if file.endswith(".csv"):
                process_stock_data(file_path, output_folder, period)
    else:
        print("Invalid input path. Please provide a valid CSV file or folder.")
        sys.exit(1)

if __name__ == "__main__":
    main()
