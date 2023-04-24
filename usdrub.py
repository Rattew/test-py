import json
import requests
import time
import datetime
from prettytable import PrettyTable

url = 'https://query2.finance.yahoo.com/v7/finance/quote?symbols=RUB=X'
hdr = {'User-Agent': 'Mozilla/5.0'}

def get_value():
    page = requests.get(url, headers=hdr).json()
    a = page['quoteResponse']['result'][0]
    b = a['regularMarketPrice']
    c = a['regularMarketChange']
    dt = datetime.datetime.now().strftime('%H:%M')
    return dt, b, c
    
def ticker(table):
    while True:
        data = get_value()
        table.add_row([data[0], data[1], data[2]])
        print(table)
        time.sleep(600)

def main():
    tbl = ["Time", "Price", "Change"]
    columns = len(tbl)
    table = PrettyTable(tbl)
    ticker(table)
    
if __name__ == '__main__' :
    main()



