#Computational Thinking
#Homework 3 - Updating your Investment Portfolio
from bs4 import BeautifulSoup
import requests
import time
import csv
from datetime import datetime
 
# Part A: Webscraping #
def get_html(url):
    response = requests.get(url)
    htmlDoc = response.text
    return htmlDoc
        
def extract_info(html,ticker):
    htmlDoc = get_html(html+ticker)
    soup = BeautifulSoup(htmlDoc,'lxml')
    Dict = {}
    fullName = soup.h1
    if fullName==None:
        return None
    else:
        Dict['Name'] = fullName.text
    time.sleep(2)
    stock_price = soup.find_all('span', class_='Trsdu(0.3s)')[0]
    Dict['Price'] = stock_price.text
    time.sleep(2)
    recentChange = soup.find_all('span', class_='Trsdu(0.3s)')[1]
    Dict['Change'] = recentChange.text
    time.sleep(2)
    return Dict


# Part B: File I/O #
def get_stockinfo(in_file):
    file = open(in_file,'r')
    text = file.read().split('\n')
    file.close()
    
    allDict = []
    Headers = text[0].split(',')
    for row in text[1:]:
        Dict = {}
        index = 0
        row = row.split(',')
        for item in row:
            Dict[Headers[index]] = item
            index+=1
        allDict.append(Dict)
    
    for stock in allDict:
        tickerInfo = extract_info(html,stock['Symbol'])
        if tickerInfo!=None:
            newPrice = float(tickerInfo['Price'].replace(',',''))
            avgPrice = float(stock['Avg buying price'].replace(',',''))
            numStocks = float(stock['Number of stocks'])
            stock['Price'] = tickerInfo['Price']
            stock['Last change'] = tickerInfo['Change']
            stock['Price change'] = newPrice - avgPrice
            stock['Value change'] = numStocks*(newPrice - avgPrice)
        else:
            stock['Price'] = None
            stock['Last change'] = None
            stock['Price change'] = None
            stock['Value change'] = None
    return allDict

def write_stockinfo_to_csv(out_file,stock_dict):
    fields = []
    for header in stock_dict[0]:
        if header not in fields:
            fields.append(header)
            
    with open(out_file, 'w') as csvfile:  
        csvwriter = csv.writer(csvfile)  
        csvwriter.writerow(fields)
        for stock in stock_dict:
            row = []
            for key,value in stock.items():
                row.append(value)
            row[4] = '$'+str[4]
            row[7] = '$'+str[7]
            csvwriter.writerow(row)


###################################################################

html = 'https://finance.yahoo.com/quote/'
stock_dict = get_stockinfo('hw3 tickers.txt')

out_file = 'hw3 tickers update'+datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p"+'.csv')
write_stockinfo_to_csv(out_file,stock_dict)






