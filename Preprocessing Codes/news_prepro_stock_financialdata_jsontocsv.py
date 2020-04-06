import json
import requests
import pandas as pd
import pandas as np
import datetime
import calendar
import csv
from pandas.io.json import json_normalize  # package for flattening json in pandas df


def station_value(zone_name,index,response,dataType,year,writer):
    normalizedStation = json_normalize(response.json()['results'][index]['Stations'])
    data_val = normalizedStation['data']
    #print(normalizedStation)
    #print(data_val)
    #print(zone_name)

    bool_val = data_val.isnull()
    print(bool_val)
    for i in range(0, len(data_val)):
        if (bool_val[i] == True):
            print(i)
            data_val[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            print(data_val[i])

    for i in range(0, len(data_val)):
        for j in range(0, 11):
            print("Zone Name: %s--Station Name: %s-- Month %d-- Val: %f" % (
            zone_name,normalizedStation['stationName'][i], j + 1, data_val[i][j]))
            station= normalizedStation['stationName'][i]
            value =data_val[i][j]
            month_num= j+1
            month_abre = datetime.date(2019, month_num, 1).strftime('%b')
            writer.writerow([dataType, year, month_num, month_abre, zone_name, station, value])


def main():
######### set params #########
    json_file= pd.read_json('C:/Users/subar/Downloads/GitHub/cmpe257_ml/Cmpe257_StockAnalysis/Datasets/A_financial_stmt.json')
    json_filepath='C:/Users/subar/Downloads/GitHub/cmpe257_ml/Cmpe257_StockAnalysis/Datasets/A_financial_stmt.json'
    csv_filepath= 'C:/Users/subar/Downloads/GitHub/cmpe257_ml/Cmpe257_StockAnalysis/Datasets/A_financial_stmt.csv'
    headers = ['AirQualityIndex', 'Year', 'MonthNo', 'MonthName', 'Zone', 'Station', 'Value']

    with open(json_filepath) as data_file:
        json_data = json.load(data_file)
    f = csv.writer(open(csv_filepath,  'w', newline=''))

    # Write CSV Header, If you dont need that, remove this line
    f.writerow(["Stock", "Date","Revenue", "RevenueGrowth"])

    #print(json_data['financials'][0]['date'])
    print(len(json_data['financials']))
    for i in range(0,len(json_data['financials'])):
        print(json_data['symbol'])
        print(json_data['financials'][i]['date'])
        f.writerow([json_data['symbol'],
                    json_data['financials'][i]['date'],
                    json_data['financials'][i]['Revenue'],
                    json_data['financials'][i]['Revenue Growth']
                    ])
main()







