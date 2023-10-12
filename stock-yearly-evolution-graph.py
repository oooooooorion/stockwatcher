import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from matplotlib.dates import DateFormatter

# Check if the command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python stock_price_evolution.py <path_to_csv_file>")
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

# Extract year from the 'Date' column
df['Year'] = df['Date'].dt.year
df['DayOfYear'] = df['Date'].dt.dayofyear  # Extract the day of the year

# Group the data by year and day of the year and calculate the mean Close price for each day of the year
daily_data = df.groupby(['Year', 'DayOfYear'])['Close'].mean().reset_index()

# Create a plot
plt.figure(figsize=(12, 6))

# Loop through each year and plot the data for that year
for year in daily_data['Year'].unique():
    year_data = daily_data[daily_data['Year'] == year]
    x_values = year_data['DayOfYear']
    y_values = year_data['Close'] / year_data.iloc[0]['Close'] * 100  # Normalize to 100 on 1st January
    plt.plot(x_values, y_values, label=str(year))

# Set x-axis labels to be months
ax = plt.gca()
date_format = DateFormatter("%b")
ax.xaxis.set_major_formatter(date_format)
plt.xlabel('Month')
plt.ylabel('Normalized Close Price (1st January = 100)')
plt.title('Stock Price Evolution Year over Year')
plt.legend()
plt.grid(True)

# Save the plot as a PNG file
output_path = "stock_price_evolution.png"
plt.savefig(output_path, bbox_inches='tight')

# Show the plot (optional)
plt.show()

print(f"Stock price evolution plot saved as '{output_path}'")
