import json
import csv
import pandas as pd
from pandas.io.json import json_normalize  # package for flattening json in pandas df
import glob
import os


def parse_articles(articles):
    '''
    This function takes in a response to the NYT api and parses
    the articles into a list of dictionaries
    '''
    news = []
    for i in articles['response']['docs']:
        dic = {}
        dic['id'] = i['_id']

        dic['abstract'] = ''
        if pd.isna(i['headline']['main']):
            dic['headline'] = i['headline']['main'].encode("utf8")
        dic['desk'] = ''
        dic['date'] = i['pub_date'][0:10] # cutting time of day.
        dic['section'] = ''
        if i['snippet'] is not None:
            dic['snippet'] = i['snippet'].encode("utf8")
        if i['snippet'] is None:
            dic['snippet'] = ''
        dic['source'] = i['source']
        dic['type'] = ''
        dic['url'] = i['web_url']
        dic['word_count'] = i['word_count']
        # locations
        locations = []
        for x in range(0,len(i['keywords'])):
            if 'glocations' in i['keywords'][x]['name']:
                locations.append(i['keywords'][x]['value'])
        dic['locations'] = locations
        # subject
        subjects = []
        for x in range(0,len(i['keywords'])):
            if 'subject' in i['keywords'][x]['name']:
                subjects.append(i['keywords'][x]['value'])
        dic['subjects'] = subjects
        news.append(dic)
    return(news)


#json_file= pd.read_json('C:/Users/subar/Downloads/GitHub/cmpe257_ml/Cmpe257_StockAnalysis/Datasets/A_financial_stmt.json')
json_filepath='C:/Users/subar/Downloads/GitHub/cmpe257_ml/Cmpe257_StockAnalysis/Datasets/financial-news-json/news-json/indices/2010-03-news.json'
csv_filepath= 'C:/Users/subar/Downloads/GitHub/cmpe257_ml/Cmpe257_StockAnalysis/Datasets/financial-news-json/combined_financial_news.csv'
headers = ['id', 'abstract','headline', 'desk', 'date', 'section', 'snippet', 'source', 'type', 'url', 'word_count', 'locations', 'subjects']

path = r'C:/Users/subar/Downloads/GitHub/cmpe257_ml/Cmpe257_StockAnalysis/Datasets/financial-news-json/news-json/indices/*.json'

with open(json_filepath) as data_file:
    json_data = json.load(data_file)
    #print(json_data)

articles = parse_articles(json_data)

keys = articles[0].keys()  ##headers
#print(keys)
with open(csv_filepath, 'a', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    #dict_writer.writeheader()
    dict_writer.writerows(articles)

