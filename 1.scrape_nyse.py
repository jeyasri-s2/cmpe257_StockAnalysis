from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import time
import csv
import datetime

driver = webdriver.Firefox()
driver.get("https://www.nyse.com/listings_directory/stock")

stock_symbols = []
try:
    for i in range(646):
        print (stock_symbols)
        time.sleep(3)
        trs = driver.find_elements(By.XPATH, '//tr')
        trs = trs[1:]
        for tr in trs:
            stock_symbols.append(str(tr.text).split(" ")[0])

        next_button = driver.find_element_by_xpath(".//a[@rel='next']")
        next_button.click()
except:
    print ("Your iterations suck")

print (len(stock_symbols))

now = datetime.datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
file_write_csv = open("scrape_nyse_" + dt_string + ".csv", 'w')
file_write_csv.write("stock_symbol\n")
for stock_symbol in stock_symbols:
    file_write_csv.write(stock_symbol + "\n")

file_write_csv.close()

driver.close()