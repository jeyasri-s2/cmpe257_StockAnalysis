import glob 
import pandas as pd
import datetime

class aggregate_stock_sector_data():

    def __init__(self):
        self.stocks_files = glob.glob("../data/dataset_with_sector/*.csv")

        self.stocks_files.sort()
    
    def aggregate_data(self):
        combined_csv = []
        
        for stock_file in self.stocks_files:
            split_stock_name_sector = stock_file.split("/")[-1].split(".")[0].split("_")
            stock_name = split_stock_name_sector[0]
            sector = split_stock_name_sector[1]
            temp_pd = pd.read_csv(stock_file)
            temp_pd['stock_name'] = stock_name
            temp_pd['sector'] = sector
            
            combined_csv.append(temp_pd)
        combined_csv = pd.concat(combined_csv)
        now = datetime.datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        
        combined_csv.to_csv( "../data/aggregated_data/combined_" + dt_string + ".csv", index=False, encoding='utf-8-sig')

    def run(self):
        print ("----- Aggregating Data-----")
        self.aggregate_data()

if __name__ == "__main__":
    a_s_s_d = aggregate_stock_sector_data()
    a_s_s_d.run()