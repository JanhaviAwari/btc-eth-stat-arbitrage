
# BTC–ETH Statistical Arbitrage Project

## Overview
This project shows a simple statistical arbitrage setup using Bitcoin (BTC) and Ethereum (ETH).  
The idea is to observe how the prices of BTC and ETH move together, measure their relationship, and identify when they temporarily move away from their normal behavior.

The project includes a tool to collect live price data and a dashboard to analyze and visualize the results.

## What this project includes
The project has two main parts:

1. **Tick Collector**
   - A small desktop application with Start and Stop buttons
   - Collects live BTC and ETH prices at regular intervals
   - Allows downloading the collected data as a CSV file

2. **Analytics Dashboard**
   - Shows BTC and ETH prices in real time
   - Calculates the hedge ratio between BTC and ETH
   - Computes the spread and its Z-score
   - Displays an alert when the price difference becomes unusually large

## Data Source
- Binance public API
- Trading pairs used: BTCUSDT and ETHUSDT
- Prices are fetched at fixed time intervals to simulate live market data

## Methodology
The analysis follows these steps:

1. **Hedge Ratio**
   - A simple linear regression is used to estimate how BTC moves relative to ETH.

2. **Spread Calculation**
   - The hedge ratio is used to calculate the price spread between BTC and ETH.

3. **Z-Score**
   - The spread is normalized using a rolling mean and standard deviation.
   - This helps identify when the spread is unusually high or low.

4. **Alert Logic**
   - An alert is shown only when the Z-score goes beyond ±2.
   - This avoids reacting to small and random price movements.

## Output
- Live charts of BTC and ETH prices
- Hedge ratio and Z-score values
- Alert status (Normal or Alert)
- Downloadable CSV file containing collected price data

## How to Run the Project

### Run the Tick Collector
```bash
python tick_collector_app.py

Requirements:

# Install all required libraries using:
pip install -r requirements.txt


Future Improvements

Use WebSocket data for higher-frequency updates
Add backtesting to evaluate strategy performance
Include trade execution and risk management logic

Conclusion

This project demonstrates the basic idea behind a statistical arbitrage strategy using real market data. It focuses on clear logic, practical implementation, and easy-to-understand visualization rather than complex trading rules.
