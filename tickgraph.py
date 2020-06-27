# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 22:24:43 2020

@author: xqiao
"""

import requests
import pandas as pd

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components
from bokeh.io import save

# #receive sticker and get data
def get_df_by_sticker(inp):
    sticker= str(inp)
    #set empty df
    df=pd.DataFrame()

    #get data with symbol=inp
    bits1="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
    bits2="&apikey=96AQXV2FPIVZ1TOZ"
    # samp="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=96AQXV2FPIVZ1TOZ"
    r=requests.get (bits1+sticker+bits2)
    
    data=r.json()
    data2=pd.json_normalize(data['Time Series (Daily)'],max_level=0)
    colnm=data2.columns
    for date in colnm: #get dataframe
        out= data2[date]
        out1=pd.json_normalize(out) #5 columns
        out1['time']=date #6 column
        df=df.append(out1, ignore_index=True)
    df=pd.DataFrame(df)
    return df

#graph it
def get_a_graph(inp):
    df_s=get_df_by_sticker(inp)
    df_s['time'] = pd.to_datetime(df_s['time'])
    tmin=df_s['time'].min()
    tmax=df_s['time'].max()
    y=pd.to_numeric(pd.Series(df_s['4. close']))
    p1 = figure(x_axis_type="datetime", x_range = (tmin, tmax), y_range=(min(y),max(y)),title="Recent Stock Closing Prices")
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Close Price'
    p1.line(df_s['time'], df_s['4. close'], color='#A6CEE3', legend_label=inp)
    # save(p1, filename='templates/stock.html',resources=CDN,title='my plot')
    script, div = components(p1)
    return script, div