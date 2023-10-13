#Usage: python3 stockwatcher-core.py <input_csv_or_folder> <output_folder> <monthly/weekly>"

import os
import sys
import pandas as pd

def calculate_monthly_statistics(data):
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    monthly_data = data['Close'].resample('M').ffill()
    monthly_changes = monthly_data.diff().dropna()
    up_down = monthly_changes.apply(lambda x: 'Up' if x > 0 else 'Down')

    monthly_stats = up_down.groupby(up_down.index.month_name()).value_counts().unstack(fill_value=0)
    monthly_stats.index = monthly_stats.index.tolist()
    monthly_stats.columns = ['Up', 'Down']

    return monthly_stats

def calculate_weekly_statistics(data):
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    weekly_data = data['Close'].resample('W').ffill()
    weekly_changes = weekly_data.diff().dropna()
    up_down = weekly_changes.apply(lambda x: 'Up' if x > 0 else 'Down')

    # Use isocalendar().week to get the week number
    weekly_stats = up_down.groupby(up_down.index.isocalendar().week).value_counts().unstack(fill_value=0)
    weekly_stats.index = weekly_stats.index.tolist()
    weekly_stats.columns = ['Up', 'Down']

    return weekly_stats

def analyze_stock_data(input_path, output_path, frequency):
    if os.path.isdir(input_path):
        files = os.listdir(input_path)
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(input_path, file)
                output_file = os.path.splitext(file)[0] + f'_{frequency}_statistics.csv'
                data = pd.read_csv(file_path)
                if frequency == 'monthly':
                    stats = calculate_monthly_statistics(data)
                elif frequency == 'weekly':
                    stats = calculate_weekly_statistics(data)
                stats.to_csv(os.path.join(output_path, output_file))
    elif os.path.isfile(input_path) and input_path.endswith('.csv'):
        data = pd.read_csv(input_path)
        if frequency == 'monthly':
            stats = calculate_monthly_statistics(data)
        elif frequency == 'weekly':
            stats = calculate_weekly_statistics(data)
        output_file = os.path.splitext(os.path.basename(input_path))[0] + f'_{frequency}_statistics.csv'
        stats.to_csv(os.path.join(output_path, output_file))
    else:
        print("Invalid input path or file format.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 script.py <input_csv_or_folder> <output_folder> <monthly/weekly>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    frequency = sys.argv[3]

    if frequency not in ['monthly', 'weekly']:
        print("Frequency must be 'monthly' or 'weekly'")
        sys.exit(1)

    analyze_stock_data(input_path, output_path, frequency)
