#Execution method: ./script.sh <ticker_list_path> <output_folder_path> <start_date> [<end_date>]
#Beware the tickers in the ticker list must, for some, have a suffix (stock exchange code) after them. It is recommended to include them.
#Example: AF.PA (Air France Euronext Paris)
#Tip: You can ask ChatGPT for lists with suffixes separated by returns.
#!/bin/bash

if [ $# -lt 3 ]; then
  echo "Usage: $0 <ticker_list_path> <output_folder_path> <start_date> [<end_date>]"
  exit 1
fi

ticker_list_path=$1
output_folder=$2
start_date=$3
end_date=${4:-$(date +'%Y-%m-%d')}

# Create the output folder if it doesn't exist
mkdir -p "$output_folder"

while IFS= read -r ticker || [[ -n $ticker ]]; do
  # Run the stock scraper script for each ticker
  if python3 stockwatcher-stock-scraper-output-specified.py "$ticker" "$output_folder" "$start_date" "$end_date"; then
    echo "Scraped data for $ticker"
  else
    echo "Failed to scrape data for $ticker"
  fi
done < "$ticker_list_path"

