import csv 
import re
import yfinance as yf
import sys

print ("------ Reformat Stock Ticker ------")
stock_symbols = csv.reader(open("scrape_nyse_14_02_2020_22_26_02.csv", 'r'))
final_stock_symbols = []

for skip in stock_symbols:
    break

for stock_symbol_row in stock_symbols:
    stock_symbol = stock_symbol_row[0]

    if ".CL" in stock_symbol:
        if stock_symbol == "ARRpB.CL":
            stock_symbol = "ARR-PBCL"
        elif stock_symbol == "COFpP.CL":
            stock_symbol = "COF-PPCL"
        elif stock_symbol == "JPMpF.CL":
            stock_symbol = "JPM-PFCL"
        elif stock_symbol == "OSLE.CL":
            stock_symbol = "OSLE-CL"

    elif "." in stock_symbol:
        stock_symbol = stock_symbol.split(".")[0] + "-" + stock_symbol.split(".")[1]
    elif "p" in stock_symbol:
        split_stock_symbol = stock_symbol.split("p")
        stock_symbol = split_stock_symbol[0] + "-P" + split_stock_symbol[1]

    print (stock_symbol)
    final_stock_symbols.append(stock_symbol)

print ("------ Remove Invalid Stocks (Analysis) ------")

num_missing = []
for stock_data in final_stock_symbols:
    try:
        ticker = yf.Ticker(str(stock_data))
        sector = ticker.info['sector'] 
    except:
        e = sys.exc_info()[0]
        print (stock_data)
        print (e)
        num_missing.append(stock_data)
       
print(num_missing)
print(len(num_missing))

print ("------ Get Date,Open,High,Low,Close,Volume,OpenInt data for each stock, save in file ------")

print ("------ Final Model Script  ------")

print ("------ Add Ticker ------")

