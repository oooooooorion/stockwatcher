import pandas as pd
import sys
import os

# Check if the command-line arguments are provided
if len(sys.argv) != 3:
    print("Usage: python3 stockwatcher-monthly.py <input_csv_path/input_folder_path> <output_folder_path>")
    sys.exit(1)

input_path = sys.argv[1]
output_folder = sys.argv[2]

# Function to process a single CSV file
def process_csv(input_file, output_folder):
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"File not found: {input_file}")
        return
    except Exception as e:
        print(f"An error occurred while processing {input_file}: {str(e)}")
        return

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
    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    monthly_stats['Month'] = monthly_stats['Month'].map(lambda x: month_names[x - 1])

    # Generate the output filename
    file_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_folder, f"{file_name}_monthly_statistics.csv")

    try:
        # Write the statistics to a CSV file
        monthly_stats.to_csv(output_file, index=False)
        print(f"Monthly stock price statistics saved to '{output_file}'")
    except Exception as e:
        print(f"An error occurred while saving the statistics to {output_file}: {str(e)}")

# Check if the input is a folder
if os.path.isdir(input_path):
    for root, _, files in os.walk(input_path):
        for file in files:
            if file.endswith(".csv"):
                input_file = os.path.join(root, file)
                process_csv(input_file, output_folder)
else:
    process_csv(input_path, output_folder)
