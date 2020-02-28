import glob 
import pandas as pd
import datetime
import sys

class clean_data():

    def __init__(self):
        self.stocks_files = glob.glob("../data/dataset_with_sector/*.csv")

        self.stocks_files.sort()
    
    def update_remove_nans(self):
        
        for stock_file in self.stocks_files:
            temp_pd = pd.read_csv(stock_file)
            temp_pd['Open'].fillna((temp_pd['Open'].mean()), inplace=True)
            temp_pd['Low'].fillna((temp_pd['Low'].mean()), inplace=True)
            temp_pd['High'].fillna((temp_pd['High'].mean()), inplace=True)
            temp_pd['Close'].fillna((temp_pd['Close'].mean()), inplace=True)
            temp_pd['Volume'].fillna((temp_pd['Volume'].mean()), inplace=True)
            temp_pd.dropna(axis=1, how='any')
            temp_pd['year_str'] = temp_pd['Date'].map(lambda x: x[0:4] )
            temp_pd['month_str'] = temp_pd['Date'].map(lambda x: x[5:7] )
            temp_pd['date_str'] = temp_pd['Date'].map(lambda x: x[8:10] )
            temp_pd['year'] = temp_pd['Date'].map(lambda x: int(x[0:4]) )
            temp_pd['month'] = temp_pd['Date'].map(lambda x: int(x[5:7]) )
            temp_pd.to_csv(stock_file)
            sys.exit()

    def run(self):
        print ("----- Clean Data-----")
        self.update_remove_nans()

if __name__ == "__main__":
    c_d = clean_data()
    c_d.run()