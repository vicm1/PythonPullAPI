 #This example uses Python 2.7 and the python-request library.
# Using the quickstart code example to start off this crypto api
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from key import TOKEN # personal api key can be not shown
import pandas as pd
import os
from time import time
from time import sleep

def automated_api():
    global dataframe
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '15',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': TOKEN # import personal API key through token
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        pd.set_option('display.max_columns', None)  # Show all columns
        pd.set_option('display.max_rows', None) # allows to see all rows
        #dataframe = pd.DataFrame()
        dataframe = pd.json_normalize(data['data']) # makes data easier to read
        dataframe['timestamp'] = pd.to_datetime('now') # time when data was automated and pulled
        #dataframe = pd.concat([dataframe, dataframe2], ignore_index=True)  # Append new data to the existing DataFrame when printing, remove if adding to csv
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    
    if not os.path.isfile(r'C:\Users\capta\Desktop\Git\PythonPullAPI\cryptoAPI.csv'): # check if the csv file has not been created yet
        dataframe.to_csv(r'C:\Users\capta\Desktop\Git\PythonPullAPI\cryptoAPI.csv', header = 'column_names') # if it hasn't then create it
    else:
        dataframe.to_csv(r'C:\Users\capta\Desktop\Git\PythonPullAPI\cryptoAPI.csv', mode = 'a', header = False)

    readcsv = pd.read_csv(r'C:\Users\capta\Desktop\Git\PythonPullAPI\cryptoAPI.csv') # read the csv that was created and its added contents
    print(readcsv)

    
for i in range(333):
    automated_api()
    print('API Automation Running')
    sleep(10) 
exit()