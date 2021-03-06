import glob 
import pandas as pd
import datetime
import sys

class clean_data():

    def __init__(self):
        self.stocks_files = glob.glob("../data/dataset_with_sector/*.csv")
        self.stocks_files.sort()
    
    def store_in_clean_dir(self, stock_file):
        file_path = stock_file.split("/")
        file_path[-2] = "dataset_with_sector_clean"
        new_path = ""
        for path in file_path:
            new_path = new_path + path + "/"

        return new_path[:-1]
    def update_remove_nans(self):
        
        for stock_file in self.stocks_files:
            split_stock_name_sector = stock_file.split("/")[-1].split(".")[0].split("_")
            stock_name = split_stock_name_sector[0]
            sector = split_stock_name_sector[1].strip()
            if sector != '':
                temp_pd = pd.read_csv(stock_file)
                temp_pd['Open'].fillna((temp_pd['Open'].mean()), inplace=True)
                temp_pd['Low'].fillna((temp_pd['Low'].mean()), inplace=True)
                temp_pd['High'].fillna((temp_pd['High'].mean()), inplace=True)
                temp_pd['Close'].fillna((temp_pd['Close'].mean()), inplace=True)
                temp_pd['Volume'].fillna((temp_pd['Volume'].mean()), inplace=True)
                temp_pd.dropna(axis=1, how='any')
                temp_pd['day'] = temp_pd['Date'].map(lambda x: x[8:10] )
                temp_pd['year'] = temp_pd['Date'].map(lambda x: int(x[0:4]) )
                temp_pd['month'] = temp_pd['Date'].map(lambda x: int(x[5:7]) )
                new_stock_file = self.store_in_clean_dir(stock_file)
                temp_pd.to_csv(new_stock_file, index=False)
            else:
                print ("Skipped, no sector available", stock_file)

    def run(self):
        print ("----- Clean Data-----")
        self.update_remove_nans()

if __name__ == "__main__":
    c_d = clean_data()
    c_d.run()