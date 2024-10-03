import pandas as pd
import numpy as np
import os
import evaluation_metrics

import warnings 
warnings.filterwarnings('ignore', category=FutureWarning)

# global variables ( for testing fixed position sizing )
fixed_shares_to_buy = 100
fixed_shares_to_sell = 100

def get_data_files(data_folder='data'):
    data_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
    data_dict = {}
    for file in data_files:
        data = pd.read_csv(os.path.join(data_folder, file))
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        ticker = file[:-4]  
        data_dict[ticker] = data
    return data_dict

def calculate_rsi(data, window=20):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi
    return data

def calculate_bollinger_bands(data, window=20, num_std=2):
    data['SMA'] = data['Close'].rolling(window=window).mean()
    data['STD'] = data['Close'].rolling(window=window).std()
    data['Upper Band'] = data['SMA'] + (data['STD'] * num_std)
    data['Lower Band'] = data['SMA'] - (data['STD'] * num_std)
    data['Upper Band 2'] = data['SMA'] + (data['STD'] * num_std * 2)
    data['Lower Band 2'] = data['SMA'] - (data['STD'] * num_std * 2)
    return data

def calculate_MACD(data, short_window=12, long_window=26, signal_window=9):
    data['Short EMA'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['Long EMA'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = data['Short EMA'] - data['Long EMA']
    data['Signal Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data

def calculate_ATR(data, window=14):
    data['H-L'] = abs(data['High'] - data['Low'])
    data['H-PC'] = abs(data['High'] - data['Close'].shift(1))
    data['L-PC'] = abs(data['Low'] - data['Close'].shift(1))
    data['TR'] = data[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    data['ATR'] = data['TR'].rolling(window=window).mean()
    return data

def generate_signals(data, additional_indicators=[]):

    if additional_indicators == []:
        data['Buy Signal'] = (data['Close'] < data['Lower Band']) & (data['Close'] > data['Lower Band 2'])
        data['Sell Signal'] = (data['Close'] > data['Upper Band']) & (data['Close'] < data['Upper Band 2'])
    elif 'RSI' in additional_indicators:
        data['Buy Signal'] = (data['Close'] < data['Lower Band']) & (data['Close'] > data['Lower Band 2']) & (data['RSI'] < 40)
        data['Sell Signal'] = (data['Close'] > data['Upper Band']) & (data['Close'] < data['Upper Band 2']) & (data['RSI'] > 70)
    elif 'MACD' in additional_indicators:
        data['Buy Signal'] = (data['Close'] < data['Lower Band']) & (data['Close'] > data['Lower Band 2']) & (data['MACD'] > data['Signal Line']) & (data['MACD'].shift(1) < data['Signal Line'].shift(1))
        data['Sell Signal'] = (data['Close'] > data['Upper Band']) & (data['Close'] < data['Upper Band 2']) & (data['MACD'] < data['Signal Line']) & (data['MACD'].shift(1) > data['Signal Line'].shift(1))
    return data

def generate_portfolio(data_dict, beginning_value=10000, start_date='2013-01-01', end_date='2023-12-31', position_sizing='risk', risk_factor=0.0035, additional_indicators=[]):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    date_range = pd.date_range(start=start_date, end=end_date)

    columns = ['Cash Value', 'Holding Value', 'Total'] + list(data_dict.keys())
    portfolio = pd.DataFrame(index=date_range, columns=columns)
    portfolio.iloc[0] = [beginning_value] + [0] + [beginning_value] + [0] * len(data_dict)
    portfolio.index.name = 'Date'
    
    for ticker, data in data_dict.items():
        if 'Adj Close' in data.columns and 'Volume' in data.columns:
            data = data.drop(columns=['Adj Close', 'Volume'])
        data = calculate_bollinger_bands(data)
        data = calculate_rsi(data)
        data = calculate_ATR(data)

        data = generate_signals(data, additional_indicators)
        data_dict[ticker] = data

        # save to csv in temp folder
        if data_dict[ticker] is not None:
            if os.path.exists(f'temp/{ticker}.csv'):
                os.remove(f'temp/{ticker}.csv')
            data_dict[ticker].to_csv(f'temp/{ticker}.csv')
            continue

    for i in range(1, len(portfolio)):
        current_date = portfolio.index[i]
        prev_date = portfolio.index[i-1]

        portfolio.loc[current_date] = portfolio.loc[prev_date]

        cash_value = portfolio.loc[prev_date, 'Cash Value']
        holding_value = 0

        for ticker, data in data_dict.items():
            if current_date in data.index[:-1]:
                current_price = data.loc[current_date, 'Close'] 
                next_day_open = data.iloc[data.index.get_loc(current_date) + 1]['Open']

                current_holdings = portfolio.loc[current_date, ticker]

                if data.loc[current_date, 'Buy Signal'] and cash_value >= next_day_open:
                    if position_sizing == 'fixed':
                        shares_to_buy = min(fixed_shares_to_buy, cash_value // next_day_open)

                    if position_sizing == 'risk':
                        shares_to_buy = (risk_factor * cash_value) // data['ATR'].loc[current_date]

                    portfolio.loc[current_date:, ticker] += shares_to_buy
                    cash_value -= shares_to_buy * next_day_open

                elif data.loc[current_date, 'Sell Signal'] and current_holdings > 0:
                    if position_sizing == 'fixed':
                        shares_to_sell = min(fixed_shares_to_sell, current_holdings)

                    if position_sizing == 'risk':
                        shares_to_sell = min((risk_factor * cash_value) // data['ATR'].loc[current_date], current_holdings)

                    portfolio.loc[current_date:, ticker] -= shares_to_sell
                    cash_value += shares_to_sell * next_day_open
                holding_value += portfolio.loc[current_date, ticker] * next_day_open

        portfolio.loc[current_date, 'Cash Value'] = cash_value
        portfolio.loc[current_date, 'Holding Value'] = holding_value
        portfolio.loc[current_date, 'Total'] = cash_value + holding_value

    portfolio.iloc[:, -6:] = portfolio.iloc[:, -6:].astype(int)

    portfolio.iloc[:, :-6] = portfolio.iloc[:, :-6].round(2)    

    return portfolio

def main():
    data_dict = get_data_files()
    portfolio = generate_portfolio(data_dict)

    print("Portfolio Summary:")
    print(evaluation_metrics.evaluate_portfolio(portfolio))

    print("\nFinal Portfolio Value:")
    print(portfolio.iloc[-1])

    if os.path.exists('portfolio_versions/portfolio.csv'):
        os.remove('portfolio_versions/portfolio.csv')

    portfolio.to_csv('portfolio_versions/portfolio.csv')

    initial_value = portfolio.iloc[1]['Total']
    final_value = portfolio.iloc[-1]['Total']
    total_return = (final_value - initial_value) / initial_value * 100
    print(f"\nTotal Return: {total_return:.2f}%")

if __name__ == '__main__':
    main()