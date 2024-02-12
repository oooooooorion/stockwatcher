# stockwatcher
Remember that I'm a law student after all, not an IT one. Therefor, this project allowed me more to master ChatGPT than Python. And because barely everything has been created throught ChatGPT (3.5), I don't even know what it really does for much. The main goal of this project is to prove it is feasible to code without even knowing how to code (just a bit of tech stuff) using LLMs (and maybe to make lots of money but I'm not so sure for that). And for the record, I've written the hereby file myself.
## English guide
### Getting started
#### Cloning the repo
```$ git clone https://github.com/oooooooorion/stockwatcher.git```

```$ cd ./stockwatcher```
#### Installing dependencies
First of all, make sure you have Python and Pip (comes with Python) installed on your machine.

Install dependencies (in this case: pandas and yfinance)
```$ pip install -r requirements.txt```
### Features
Stockwatcher allows for data scraping and (very simple) market analysis. The analysis is about monthly tendencies. (Like to show if a certain stock has a tendency to go up before christmas idk)
#### stockwatcher-scrape
Stockwatcher allows users to scrape data from Yahoo! Finance (not so complicated, but annoying). 

The ```stockwatcher-scrape.py``` script can download data from one or multiple stocks/ETFs/indexes (or whatever I haven't tested). Eitherway, it allows to download data since a certain date or from one date to another.

To donwload multiple stocks' data you'll have to place your stocks' tickers in a text file, however for some reason, tickers will have to be separated with commas. (such as given in the ```./ticker-lists/``` folder).

You'll have to create a folder for stockwater-scrape output such as: 
```$ mkdir scrape-output```

Here's the full usage of the ```stockwatcher-scrape.py``` script:

For a single stock's data:

```$ python3 stockwatcher-scrape.py <ticker> </path/to/output_folder> <YYYY-MM-DD> [<YYYY-MM-DD>]```

For a multiple stocks' data:

```$ python3 stockwatcher-scrape.py </path/to/ticker/list.txt> </path/to/output_folder> <YYYY-MM-DD> [<YYYY-MM-DD>]```

Be aware that if argument```[<YYYY-MM-DD>]``` is not filled, it will be replaced by today.
#### stockwatcher-monthly
So now that you have some data, you can start to play with the full potential of stockwatcher.
Here's the usage if you know the stuff:
```$ python3 stockwatcher-monthly.py <input_csv_path/input_folder_path> <output_folder_path>```

Argument ```<input_csv_path>``` or ```<input_folder_path>``` is what we just downloaded under ```scrape-output```.

Argument ```<output_folder_path>``` you'll have to create (I do not feel the need to re-explain how to create a folder under a *nix environment) or use ```./``` if you ain't got a lot of input files.
Then see the result yourself (or look inside the ```example``` folder you fool).
#### other stuff: working-old folder
Here you have interesting stuff that worked or barely worked. Such as ```stock-yearly-evolution-graph.py``` which creates a cool graph starting at 0,0 every January 1st of every year to compare the graph years over years.

## Guide en français
vindra un jour ptet
