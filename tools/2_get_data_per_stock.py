import csv 
import re
import yfinance as yf
import sys
import os.path
import glob 

class get_data_per_stock():
    
    def __init__(self):
        self.stocks_files = glob.glob("../data/dataset_with_sector/*.csv")
        self.stock_symbols = csv.reader(open("../data/scraped_stocks/scrape_nyse_14_02_2020_22_26_02.csv", 'r'))

        for skip in self.stock_symbols:
            break

    def reformat_stock_symbols(self):
        self.reformated_stock_symbols = []
        for stock_symbol_row in self.stock_symbols:
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

            self.reformated_stock_symbols.append(stock_symbol)

    def remove_invalid_stocks(self):

        stocks_to_remove_csv = csv.reader(open("../data/data_to_avoid/need_to_remove.csv", 'r'))

        for skip in stocks_to_remove_csv:
            break

        ones_to_remove = []
        self.final_stock_symbols = []

        for s_t_r_c in stocks_to_remove_csv:
            stock_symbol = s_t_r_c[0]
            ones_to_remove.append(stock_symbol)

        for r_s_s in self.reformated_stock_symbols:
            if r_s_s not in ones_to_remove:
                self.final_stock_symbols.append(r_s_s)

        """
            This next portion is commented out because it takes a while to run. We saved the results of that and 
            put it in data/data_to_avoid. Left it in case we needed to rerun
        """
        # num_missing = []
        # for stock_data in self.reformated_stock_symbols:
        #     try:
        #         ticker = yf.Ticker(str(stock_data))
        #         sector = ticker.info['sector'] 
        #     except:
        #         e = sys.exc_info()[0]
        #         print (stock_data)
        #         print (e)
        #         num_missing.append(stock_data)
            
        # print(num_missing)
        # print(len(num_missing))
    
    def check_if_stock_file_exists(self, cur_stock_symbol):
        for stock in self.stocks_files:
            stock_name = stock.split("/")[-1].split(".")[0].split("_")[0]
            if stock_name == cur_stock_symbol:
                return True
        
        return False
    def get_csv_data_for_stocks(self):
        
        for stock_symbol in self.final_stock_symbols:
            
            if self.check_if_stock_file_exists(stock_symbol):
                continue
            
            try:
                ticker = yf.Ticker(str(stock_symbol))
                sector = ticker.info['sector'] 
                history = ticker.history(start="2010-01-01", end="2020-01-01")
                history.to_csv("../data/dataset_with_sector/" + stock_symbol + "_" + sector.replace(" ", "-") + ".csv")
            except:
                e = sys.exc_info()[0]
                print (stock_symbol)
                print (e)
    
    def run(self):
        print ("----- Reformatting Stock Symbols -----")
        self.reformat_stock_symbols()
        print ("----- Removing Bad Stocks -----")
        self.remove_invalid_stocks()
        print ("----- Downloading CSV Data For Stocks -----")
        self.get_csv_data_for_stocks()

if __name__ == "__main__":
    g_d_p_s = get_data_per_stock()
    g_d_p_s.run()