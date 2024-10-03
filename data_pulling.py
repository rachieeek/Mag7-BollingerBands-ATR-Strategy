import yfinance
import os

'''
This module is responsible for pulling data from Yahoo Finance API, and calculating the technical indicator needed for analysis.
'''

def get_stock_data(ticker, start_date, end_date):
    stock_data = yfinance.download(ticker, start=start_date, end=end_date)
    return stock_data

def main():
    mag_7 = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'NVDA', 'TSLA', 'META']
    start_date = '2012-12-01' # start one month before the first trading day of 2013
    end_date = '2023-12-31'

    stock_data_dict = {}
    for ticker in mag_7:
        stock_data_dict[ticker] = get_stock_data(ticker, start_date, end_date)

        # save to csv in data folder
        if os.path.exists(f'data/{ticker}.csv'):
            os.remove(f'data/{ticker}.csv')

        stock_data_dict[ticker].to_csv(f'data/{ticker}.csv')
        continue

if __name__ == '__main__':
    main()