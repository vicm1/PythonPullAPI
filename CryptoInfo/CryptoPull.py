from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
#from key import TOKEN # personal api key can be not shown
import pandas as pd
import os
from time import time
from time import sleep
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Using the quickstart code example to start off this crypto api
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
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    


    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.max_rows', None) # allows to see all rows
    #dataframe = pd.DataFrame()
    dataframe = pd.json_normalize(data['data']) # makes data easier to read
    dataframe['timestamp'] = pd.to_datetime('now') # time when data was automated and pulled
    #dataframe = pd.concat([dataframe2], ignore_index=True)  # Append new data to the existing DataFrame when printing

    if not os.path.isfile(r'C:\Users\capta\Desktop\Git\PythonPullAPI\CryptoInfo\cryptoAPI.csv'): # check if the csv file has not been created yet 
        dataframe.to_csv(r'C:\Users\capta\Desktop\Git\PythonPullAPI\CryptoInfo\cryptoAPI.csv', header = 'column_names') # if it hasn't then create it 
    else:
        dataframe.to_csv(r'C:\Users\capta\Desktop\Git\PythonPullAPI\CryptoInfo\cryptoAPI.csv', mode = 'a', header = False)

    readcsv = pd.read_csv(r'C:\Users\capta\Desktop\Git\PythonPullAPI\CryptoInfo\cryptoAPI.csv') # read the csv that was created and its added contents
    pd.set_option('display.float_format', lambda x: '%.5f' % x)
    dataframe3 = dataframe.groupby('name', sort=False)[['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d', 'quote.USD.percent_change_60d','quote.USD.percent_change_90d']].mean() # average of percent change of crypto prices depending on the time frame
    dataframe4 = dataframe3.stack() #make data more consice 
    dataframe5 = dataframe4.to_frame(name='values')
    dataframe5.count() # get the count of how many values are inside df3 which is 90
    index = pd.Index(range(90)) 
    #dataframe6 = dataframe5.set_index() # set the index
    dataframe6 = dataframe5.reset_index() # reset it to show the correct values
    dataframe7 = dataframe6.rename(columns={'level_1': 'percent_change'})
    dataframe7['percent_change'] = dataframe7['percent_change'].replace(['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d', 'quote.USD.percent_change_60d','quote.USD.percent_change_90d'],['1hr','24hr','7d','30d','60d','90d']) # change names of variables to make graph more readable
    dataframe8 = dataframe[['name','quote.USD.price', 'timestamp']]
    sns.catplot(x='percent_change', y='values', hue='name', data = dataframe7, kind = 'point')
    plt.xlabel("Timeframe") # change x label of graph to Timeframe to show the percentange change from certain times
    plt.ylabel("Percent Change") # change y label of graph to Percent Change to change in percentages of crypo price
    plt.title("CryptoPull") # set name of the graph title to crypto pull
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f'{y:.2f}%'))
    plt.show() # show the graph
    print(dataframe8)

    
for i in range(333):
    automated_api()
    print('API Automation Running')
    sleep(10) 
exit()