'''
This module creates evaluation metrics for portfolio. 
'''
import pandas as pd
import numpy as np

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

def sharpe_ratio(portfolio):
    '''
    Calculate the Sharpe ratio of the portfolio.

    Parameters:
    portfolio (pd.DataFrame): The portfolio DataFrame.

    Returns:
    float: The Sharpe ratio of the portfolio.
    '''
    daily_returns = portfolio['Total'].pct_change()
    sharpe_ratio = (daily_returns.mean() - 0.02) / daily_returns.std()
    return sharpe_ratio

def annual_return(portfolio):
    '''
    Calculate the annual return of the portfolio.

    Parameters:
    portfolio (pd.DataFrame): The portfolio DataFrame.

    Returns:
    float: The annual return of the portfolio.
    '''
    total_return = (portfolio['Total'].iloc[-1] - portfolio['Total'].iloc[0]) / portfolio['Total'].iloc[0]

    years = (portfolio.index[-1] - portfolio.index[0]).days / 365
    annual_return = (1 + total_return) ** (1 / years) - 1
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

def sortino_ratio(portfolio):
    '''
    Calculate the Sortino ratio of the portfolio.

    Parameters:
    portfolio (pd.DataFrame): The portfolio DataFrame.

    Returns:
    float: The Sortino ratio of the portfolio.
    '''
    daily_returns = portfolio['Total'].pct_change()
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
    cumulative_returns = (1 + portfolio['Total'].pct_change()).cumprod()
    max_drawdown = (cumulative_returns / cumulative_returns.cummax() - 1).min()
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
        'Sharpe Ratio': sharpe_ratio(portfolio),
        'Sortino Ratio': sortino_ratio(portfolio),
        'Max Drawdown': max_drawdown(portfolio)
    }

    return evaluation_metrics


def main():
    # get portfolio to evaluate
    portfolio = pd.read_csv('portfolio_versions/portfolio.csv')
    portfolio.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
    print(portfolio.head())

    evaluation_metrics = evaluate_portfolio(portfolio)
    print("Evaluation Metrics:")
    for metric, value in evaluation_metrics.items():
        print(f"{metric}: {value:.4f}")

if __name__ == '__main__':
    main()
