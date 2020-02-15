import glob
import csv
import datetime
import sys
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class stock_summary_data():
    
    def __init__(self):
        self.stocks_files = glob.glob("/Users/wasaequreshi/Desktop/Cmpe257_StockAnalysis/dataset_with_sector/*.csv")

        self.stocks_files.sort()

    def calculate_sum_annual_return(self, file_path):
        
        sum_annual_return = 0
        each_annual_return = []

        data = pd.read_csv(file_path)
        data['year'] = data.apply(lambda row: (row.Date.split("-")[0]), axis=1)
        data = data[data['year'] >= '2010']
        
        start_date = int(data.iloc[0]['year'])
        end_date = int(data.iloc[-1]['year'])
        

        years_to_loop = int(end_date) - int(start_date) + 1
        
        for i in range(years_to_loop):
            # print (start_date)
            d_year = data[data['year'] == str(start_date) ]
             
            first_price = d_year.iloc[0]
            last_price = d_year.iloc[-1]
            
            temp_a_r = ((float(last_price['Close']) - float(first_price['Open']))/float(first_price['Open']))
            
            each_annual_return.append(temp_a_r)
            
            sum_annual_return = sum_annual_return + temp_a_r
            
            start_date = start_date + 1
        avg_yearly_return = sum_annual_return/years_to_loop
        variance_sum = 0

        for each_a_r in each_annual_return:
            variance = pow(each_a_r - avg_yearly_return, 2)
            variance_sum = variance_sum + variance
        variance_sum = variance_sum/years_to_loop
        
        return avg_yearly_return, variance_sum
    
    def run(self):
        final_data = []
        
        number_of_stocks = 0
        stocks_passed = 0
        stocks_failed = 0
        print ("----- Calculating ------")
        # Stock name, annual return (summed), variance
        for file_path in self.stocks_files:
            try:
                split_stock_name_sector = file_path.split("/")[-1].split(".")[0].split("_")
                stock_name = split_stock_name_sector[0]
                sector = split_stock_name_sector[1]
                avg_yearly_return, variance_sum = self.calculate_sum_annual_return(file_path)
                final_data.append([sector, stock_name, avg_yearly_return, variance_sum]) 
                stocks_passed = stocks_passed + 1
            except:
                
                e = sys.exc_info()[0]
                print ("Error")
                print (stock_name)
                print (e)
                stocks_failed = stocks_failed + 1
            number_of_stocks = number_of_stocks + 1
        
        now = datetime.datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

        file_write_csv = open("stock_summary_data_" + dt_string + ".csv", 'x')
        file_write_csv.write("sector,stock_name,avg_yearly_return,variance_sum\n")
        print ("----- Writing ------")
        for stock_data in final_data:
            try:
                file_write_csv.write(str(stock_data[0]) + "," + str(stock_data[1]) + "," + str(stock_data[2]) + "," + str(stock_data[3]) + "\n")
            except:
                print (stock_data)
        file_write_csv.close()
if __name__ == "__main__":

    ssd = stock_summary_data()
    ssd.run()