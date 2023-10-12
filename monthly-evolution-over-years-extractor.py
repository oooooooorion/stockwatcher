import pandas as pd
import sys

# Check if the command-line argument is provided
if len(sys.argv) != 3:
    print("Usage: python stock_price_statistics.py <path_to_csv_file> <output_csv_file>")
    sys.exit(1)

# Read the CSV file into a Pandas DataFrame
csv_path = sys.argv[1]
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    print(f"File not found: {csv_path}")
    sys.exit(1)

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Extract year and month from the 'Date' column
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Group the data by year and month and calculate the first and last Close price for each month
monthly_data = df.groupby(['Year', 'Month'])['Close'].agg(['first', 'last']).reset_index()

# Calculate whether the stock price increased or decreased for each month
monthly_data['PriceChange'] = monthly_data['last'] - monthly_data['first']
monthly_data['Up'] = monthly_data['PriceChange'] > 0
monthly_data['Down'] = monthly_data['PriceChange'] < 0

# Group the data by month and calculate the number of months that had an increase and decrease
monthly_stats = monthly_data.groupby('Month')[['Up', 'Down']].sum().reset_index()

# Map month numbers to month names
month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
monthly_stats['Month'] = monthly_stats['Month'].map(lambda x: month_names[x - 1])

# Write the statistics to a CSV file
output_csv_path = sys.argv[2]
monthly_stats.to_csv(output_csv_path, index=False)

print(f"Monthly stock price statistics saved to '{output_csv_path}'")
