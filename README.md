# Mag7-BollingerBands-ATR-Strategy

# Magnificent 7 Backtesting Project

This project evaluates the performance of seven key stocks in the US stock market, collectively known as the "Magnificent 7" — Microsoft (MSFT), Apple (AAPL), Nvidia (NVDA), Amazon (AMZN), Google (GOOG), Meta (META), and Tesla (TSLA) — using a backtesting approach. The strategy implemented is the Double Bollinger Bands (DBB) strategy, a well-known technical indicator-based trading method, to generate buy and sell signals. The project aims to simulate trading these stocks over a historical period (2013-01-01 to 2023-12-31) and assess performance using several key metrics.

## Project Structure

```
- data_pulling.oy         # Python file to pull Mag7 historical data from yfinance
- get_portfolio.py        # Core script for running the backtest and generating the portfolio
- evaluation_metrics.py   # Python file to store portfolio evaluation metrics
- data/                   # Folder to store historical price data (fetched using Yahoo Finance API)
- portfolio_versions/     # Folder that stores last generated portfolio used for analysis
- analysis/               # Folder that stores notebooks used for portfolio evaluation
```

## Table of Contents

1. [Project Overview](#project-overview)
2. [Strategy Implementation](#strategy-implementation)
3. [Performance Metrics](#performance-metrics)
4. [Results](#results)
5. [Usage](#usage)

## Project Overview

This project implements a trading backtest for the Magnificent 7 stocks using the Double Bollinger Bands strategy. The steps involved in this project are as follows:

1. **Extract Historical Data**: Using the Yahoo Finance API, historical price data for the Magnificent 7 is fetched from 2012-31-01 to 2023-12-31.

2. **Strategy**: This strategy uses two sets of Bollinger Bands, which consist of a simple moving average (SMA) and two standard deviations above and below this average. Trading signals are generated based on the position of the stock price relative to these bands. The code includes two position sizing options - fixed or risk based (ATR).

3. **Backtesting Loop**: A trading simulation is performed assuming an initial capital of $10,000 and a minimum transaction size of 1 share per trade. The program evaluates how well the strategy performs over time using various performance metrics.

4. **Performance Metrics**: The backtesting results are evaluated using Total Return, Annual Return, Annual Volatility, Sharpe Ratio, Sortino Ratio, and Maximum Drawdown.

## Strategy Implementation

### 1. Double Bollinger Bands Strategy

The Double Bollinger Bands (DBB) strategy is used to generate buy and sell signals. This strategy employs two sets of Bollinger Bands:
- **Upper Band (1)**: 1 standard deviation above the 20-day moving average.
- **Upper Band (2)**: 2 standard deviations above the 20-day moving average.
- **Lower Band (1)**: 1 standard deviation below the 20-day moving average.
- **Lower Band (2)**: 2 standard deviations below the 20-day moving average.

**Trading Signals**:
- **Buy Signal**: When the stock price moves above the Upper Band (1) but below the Upper Band (2).
- **Sell Signal**: When the stock price moves below the Lower Band (1) but stays above the Lower Band (2).

### 2. Risk Based Position Sizing using ATR

   \[
   \text{Position Size} = \frac{\text{Risk Capital}}{\text{ATR}}
   \]
   Where the risk capital is defined as:
   \[
   \text{Risk Capital} = \text{Risk Factor} \times \text{Portfolio Value}
   \]

The Average True Range (ATR) risk position sizing strategy uses the ATR indicator to dynamically determine the number of shares to buy or sell based on market volatility. The ATR measures the average volatility over a specified period, giving an indication of how much a stock typically moves during that time. This volatility-adjusted position sizing ensures that trades are adjusted according to the current market risk.

Risk Factor: A predefined risk factor is chosen as a parameter value to determine how much capital to risk on any given trade. This means that only a fixed percentage of the portfolio is put at risk based on the stock's volatility, making the strategy more robust during periods of high volatility.

### 3. Backtesting Parameters
- **Initial Capital**: $10,000
- **Date Range**: 2013-01-01 to 2023-12-31
- **Position Sizing Method**: Fixed or Risk Based (ATR)
- **Risk Factor**: A value of 0.0035 is chosen, meaning that 0.35% of the portfolio value is at risk in each trade.

## Performance Metrics

The performance of the backtest is measured using the following metrics:

1. **Total Return**: The overall return generated from the trading strategy.
2. **Annual Return**: The average yearly return of the strategy.
3. **Annual Volatility**: The volatility of returns over the year.
4. **Sharpe Ratio**: A risk-adjusted return metric calculated as the average return divided by the standard deviation of returns.
5. **Sortino Ratio**: Similar to the Sharpe Ratio, but only considers downside risk.
6. **Maximum Drawdown**: The largest percentage drop in portfolio value from peak to trough.

## Analysis and Conclusion

After running the backtest, you can find the results in the `analysis/` folder, which will include:
- Visualizations of each stock price.
- Plots visualizing stock price movements along with the buy/sell signals.
- Analysis to determine best risk factor to trade with
- Portfolio price movement and summary
- Comparison of portfolio with the S&P500 index performance

## Usage

To run the backtest and generate the portfolio performance evaluation, use:

```bash
python get_portfolio.py
```

This will perform the backtest on the Magnificent 7 stocks using the DBB + ATR strategy and save the portfolio in the `portfolio_versions/` folder.

Feel free to reach out with any questions or suggestions for improvements!