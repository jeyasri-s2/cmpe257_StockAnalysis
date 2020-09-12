# Cmpe257_StockAnalysis
This repository will contain all notebooks created for Stock analysis Project

1. Identify the top 3 sector
> From the historical stock market data, we have identified the largest sectors by volume of stocks

2. Identify the top 5 stocks from each sector
> From the top 3 sectors identified, we computed market capitalization to identify the market leaders in the respective sectors. In total, we ended up with 15 stocks. (3 sectors * 5 stocks) 

3. Predict the stability of stocks
> Using the Random Forest algorithm, we have determined the stability of each stock from the 15 identified stocks from annual financial growth of the company and annual stock market growth 
4. Predict the growth of stocks
> Using LDA and XGBoost algorithms, we were able to determine the impact in stock growth from news sentiments

**Real-world Usecase**
Given a company's annual growth and stock's annual performace in market, we can determine the risk of investment. 
Given a news sentiment and current stock's value, we can determine the return on investment value of the stock.  
