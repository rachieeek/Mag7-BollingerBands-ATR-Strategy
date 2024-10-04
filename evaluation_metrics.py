'''
This module creates evaluation metrics for portfolio. 
'''
import pandas as pd
import numpy as np
from data_pulling import get_risk_free_rate


def total_return(portfolio):
    '''
    Calculate the total return of the portfolio.

    Parameters:
    portfolio (pd.DataFrame): The portfolio DataFrame.

    Returns:
    float: The total return of the portfolio.
    '''
    total_return = (portfolio['Total'].iloc[-1] - portfolio['Total'].iloc[0]) / portfolio['Total'].iloc[0]
    total_return = total_return * 100
    return total_return

def annual_return(portfolio):
    '''
    Calculate the annual return of the portfolio.

    Parameters:
    portfolio (pd.DataFrame): The portfolio DataFrame.

    Returns:
    float: The annual return of the portfolio.
    '''
    total_return = (portfolio['Total'].iloc[-1] - portfolio['Total'].iloc[0]) / portfolio['Total'].iloc[0]

    years = len(portfolio.resample('YE').mean())

    annual_return = ((1 + total_return) ** (1 / years) - 1) * 100
    return annual_return

def annual_volatility(portfolio):
    '''
    Calculate the annual volatility of the portfolio.

    Parameters:
    portfolio (pd.DataFrame): The portfolio DataFrame.

    Returns:
    float: The annual volatility of the portfolio.
    '''
    daily_returns = portfolio['Total'].pct_change()
    annual_volatility = daily_returns.std() * np.sqrt(252)
    return annual_volatility

def sharpe_ratio(portfolio, risk_free_rate_df):
    '''
    Calculate the Sharpe ratio of the portfolio.

    Parameters:
    portfolio (pd.DataFrame): The portfolio DataFrame with a 'Date' column and 'Total' value.
    risk_free_rate_df (pd.DataFrame): DataFrame containing risk-free rate for each day (daily rates).

    Returns:
    pd.Series: The Sharpe ratio for each year.
    '''

    risk_free_rate_df.index = pd.to_datetime(risk_free_rate_df.index)
    portfolio.index = pd.to_datetime(portfolio.index)
    portfolio = portfolio.join(risk_free_rate_df['Close'], how='left')


    daily_returns = portfolio['Total'].pct_change() *100

    daily_risk_free_rate = portfolio['Close'] / 252

    excess_returns = daily_returns - daily_risk_free_rate

    annual_sharpe_ratio = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252)

    return annual_sharpe_ratio

def sortino_ratio(portfolio, risk_free_rate_df):
    '''
    Calculate the Sortino ratio of the portfolio.

    Parameters:
    portfolio (pd.DataFrame): The portfolio DataFrame.

    Returns:
    float: The Sortino ratio of the portfolio.
    '''

    risk_free_rate_df.index = pd.to_datetime(risk_free_rate_df.index)
    portfolio.index = pd.to_datetime(portfolio.index)
    portfolio = portfolio.join(risk_free_rate_df['Close'], how='left')

    daily_returns = portfolio['Total'].pct_change() * 100

    downside_returns = daily_returns[daily_returns < 0]
    sortino_ratio = (daily_returns.mean() - 0.02) / downside_returns.std()
    return sortino_ratio

def max_drawdown(portfolio):
    '''
    Calculate the maximum drawdown of the portfolio.

    Parameters:
    portfolio (pd.DataFrame): The portfolio DataFrame.

    Returns:
    float: The maximum drawdown of the portfolio.
    '''
    cumulative_returns = (1 + portfolio['Total'].pct_change()).cumprod()-1
    wealth_index = 100 * (1 + cumulative_returns)
    previous_peaks = wealth_index.cummax()
    max_drawdown = (wealth_index - previous_peaks) / previous_peaks

    max_drawdown = max_drawdown.min()

    return max_drawdown

def evaluate_portfolio(portfolio):
    '''
    Evaluate the performance of the portfolio using various metrics.

    Parameters:
    portfolio (pd.DataFrame): The portfolio DataFrame.

    Returns:
    dict: A dictionary of evaluation metrics.
    '''
    if 'Date' in portfolio.columns:
        portfolio.set_index('Date', inplace=True)

    evaluation_metrics = {
        'Total Return': total_return(portfolio),
        'Annual Return': annual_return(portfolio),
        'Annual Volatility': annual_volatility(portfolio),
        'Sharpe Ratio': sharpe_ratio(portfolio, get_risk_free_rate('2012-12-01', '2023-12-31')),
        'Sortino Ratio': sortino_ratio(portfolio, get_risk_free_rate('2012-12-01', '2023-12-31')),
        'Max Drawdown': max_drawdown(portfolio)
    }

    return evaluation_metrics

def main():
    portfolio = pd.read_csv('portfolio_versions/portfolio.csv')
    portfolio.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
    portfolio['Date'] = pd.to_datetime(portfolio['Date'])
    evaluation_metrics = evaluate_portfolio(portfolio)
    print("Evaluation Metrics for Saved Portfolio Version:")
    for metric, value in evaluation_metrics.items():
        print(f"{metric}: {value:.4f}")

if __name__ == '__main__':
    main()
