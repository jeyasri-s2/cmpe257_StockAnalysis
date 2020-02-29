import glob
import csv
import datetime
import sys
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import traceback

class stock_summary_data():
    
    def __init__(self):
        self.stocks_files = glob.glob("../data/dataset_with_sector_clean/*.csv")
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
            try:
                # print (start_date)
                d_year = data[data['year'] == str(start_date) ]
            
                first_price = d_year.iloc[0]
                last_price = d_year.iloc[-1]
                
                temp_a_r = ((float(last_price['Close']) - float(first_price['Open']))/float(first_price['Open']))
                
                each_annual_return.append(temp_a_r)
                
                sum_annual_return = sum_annual_return + temp_a_r
                
                start_date = start_date + 1
            except:
                start_date = start_date + 1
        avg_yearly_return = sum_annual_return/len(each_annual_return)
        variance_sum = 0

        for each_a_r in each_annual_return:
            variance = pow(each_a_r - avg_yearly_return, 2)
            variance_sum = variance_sum + variance
        variance_sum = variance_sum/len(each_annual_return)
        
        return avg_yearly_return, variance_sum
    
    # Copied overall_change from https://www.geeksforgeeks.org/overall-percentage-change-from-successive-changes/
    # Python implementation of above approach 
    def overall_change(self, arr, N): 
        result = 0; 
    
        var1 = arr[0]; 
        var2 = arr[1]; 
        
        # Calculate successive change of 1st 2 change 
        result = float(var1 + var2 + 
                (float(var1 * var2) / 100)); 
    
        # Calculate successive change 
        # for rest of the value 
        for i in range(2, N): 
            result = (result + arr[i] + (float(result * arr[i]) / 100)); 
            
        return result; 

    def calculate_market_cap_overall_change(self, file_path):
        each_year_market_cap = []

        data = pd.read_csv(file_path)
        data['year'] = data.apply(lambda row: (row.Date.split("-")[0]), axis=1)
        data = data[data['year'] >= '2010']
        
        start_date = int(data.iloc[0]['year'])
        end_date = int(data.iloc[-1]['year'])
        

        years_to_loop = int(end_date) - int(start_date) + 1

        for i in range(years_to_loop):
            try:
                d_year = data[data['year'] == str(start_date) ]
                last_price = d_year.iloc[-1]
                
                temp_m_c = ((float(last_price['Volume'])*float(last_price['Close']) ))
                
                each_year_market_cap.append(temp_m_c)
                
                start_date = start_date + 1
            except:
                start_date = start_date + 1
        previous_market_cap = None
        market_cap_percent_change = []

        for i in range(len(each_year_market_cap)):
            cur_market_cap = each_year_market_cap[i]
            if previous_market_cap:
                result = (cur_market_cap - previous_market_cap)/abs(previous_market_cap) 
                market_cap_percent_change.append(result * 100) 
            previous_market_cap = cur_market_cap
        overall_change_market_cap = self.overall_change(market_cap_percent_change, len(market_cap_percent_change))
        
        return overall_change_market_cap        
    
    def put_data_together(self):
        
        self.final_data = []
        
        number_of_stocks = 0
        stocks_passed = 0
        stocks_failed = 0

        # Stock name, annual return (summed), variance
        for file_path in self.stocks_files:
            try:
                split_stock_name_sector = file_path.split("/")[-1].split(".")[0].split("_")
                stock_name = split_stock_name_sector[0]
                sector = split_stock_name_sector[1]
                if sector == "Financial":
                    sector = "Financial-Services"
                
                avg_yearly_return, variance_sum = self.calculate_sum_annual_return(file_path)
                overall_change_market_cap = self.calculate_market_cap_overall_change(file_path)
                self.final_data.append([sector, stock_name, avg_yearly_return, variance_sum, overall_change_market_cap]) 
                stocks_passed = stocks_passed + 1
            except:
                e = sys.exc_info()[0]
                print ("Error")
                traceback.print_exc()
                print (stock_name)
                print (e)
                stocks_failed = stocks_failed + 1
            number_of_stocks = number_of_stocks + 1

    def write_data(self):
        
        now = datetime.datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

        file_write_csv = open("../data/summarized_data/stock_summary_data_" + dt_string + ".csv", 'w')
        file_write_csv.write("sector,stock_name,avg_yearly_return,variance_sum,overall_change_market_cap\n")
        
        for stock_data in self.final_data:
            try:
                file_write_csv.write(str(stock_data[0]) + "," + str(stock_data[1]) + "," + str(stock_data[2]) + "," + str(stock_data[3]) + "," + str(stock_data[4]) + "\n")
            except:
                print (stock_data)
        file_write_csv.close()

        print ("../data/summarized_data/stock_summary_data_" + dt_string + ".csv")

    def run(self):
        print ("----- Putting Data Together -----")
        self.put_data_together()
        print ("----- Writing Data -----")
        self.write_data()

if __name__ == "__main__":

    ssd = stock_summary_data()
    ssd.run()