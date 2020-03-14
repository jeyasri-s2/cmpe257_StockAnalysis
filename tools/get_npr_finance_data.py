from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import time
import csv
import datetime
import traceback
import pandas as pd

from bs4 import BeautifulSoup
import urllib.request



class get_npr_finance_data():

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.npr.org/sections/business/")
        # self.scraped_articles = []
        column_names = ["title","link","date","whole_story"]
        self.df = pd.DataFrame(columns = column_names) 
    def scrape_site(self):
        
        offset = 0
        is_2020 = True
        while(is_2020):
            time.sleep(2.5)
            try:
                more_articles_button = self.driver.find_element_by_class_name('options__load-more')
                article_title = self.driver.find_elements_by_css_selector('div.item-info h2.title a')                
                
                for i in range(offset, len(article_title)):
                    title = article_title[i].text
                    
                    link = article_title[i].get_attribute('href')

                    # 
                    url = link
                    print (link)
                    content = urllib.request.urlopen(url).read()

                    soup = BeautifulSoup(content, features="lxml")
                    
                    try:
                        date = soup.find('span', attrs={"class":"date"})
                        date = date.text
                    except:
                        print ("date issues")
                        continue

                    if "2020" not in date:
                        is_2020 = False
                        break

                    story = soup.find('div', attrs={"id":"storytext"})
                    para = story.find_all('p')
                    whole_story = ""
                    for i in para:
                        whole_story = whole_story + " " + i.text
                    # 
                    self.df = self.df.append({'title' : title , 'link' : link, 'date': date, 'whole_story': whole_story} , ignore_index=True)
                
                offset = len(article_title)

                print (self.df)
                print (len(self.df))
                print (offset)
                more_articles_button.click()
            except:
                traceback.print_exc()
                print ("Error :]")

        now = datetime.datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        self.df.to_csv("../data/scraped_npr_news_articles/scrape_npr_news_" + dt_string + ".csv", index=False, encoding='utf-8-sig')
        # file_write_csv = open("../data/scraped_npr_news_articles/scrape_npr_news_" + dt_string + ".csv", 'w')
        # file_write_csv.write("title,link,date,whole_story\n")
        # for article_info in self.scraped_articles:
        #     file_write_csv.write(article_info[0] + "," + article_info[1] + "," + article_info[2] + "," + article_info[3] + "\n")

        # file_write_csv.close()
    
    def run(self):
        print ("----- Scraping Site -----")
        self.scrape_site()
       

if __name__ == "__main__":
    sn = get_npr_finance_data()
    sn.run()