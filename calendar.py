# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 16:15:40 2023

@author: USER
"""

import datetime
import pandas as pd

import requests
import streamlit as st 
import datetime as dt


st.header("Financial Report Calendar")
uploaded_file = st.file_uploader("Please Upload Excel File Here", type=["csv"])

if uploaded_file is not None:
    barry_list = pd.read_csv(uploaded_file, header=None)
else:
    barry_list = pd.read_csv("List_barry_Feb.csv", header=None)       
barry_list.columns = ["symbol"]


# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
CSV_URL = 'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey=QE8EMF2BQZL1ZM2L'
df = pd.read_csv(CSV_URL)

calendar_list = pd.merge(barry_list, df, on='symbol', how='left')
calendar_list.drop_duplicates(subset='symbol',keep='first',inplace=True)

calendar_list.sort_values(by='reportDate', ascending=True, inplace=True)
calendar_list.rename(columns={'estimate': 'EPS (estimate)'}, inplace=True)
calendar_list

calendar_list['reportDate'] = pd.to_datetime(calendar_list['reportDate'])

# Filter data within this week
with st.expander("Announce this week"):
    this_week = calendar_list[(calendar_list['reportDate'] >= dt.datetime.combine(dt.datetime.today().date(), dt.time.min) - dt.timedelta(days=dt.datetime.today().weekday())) &
               (calendar_list['reportDate'] <= dt.datetime.combine(dt.datetime.today().date(), dt.time.min) + dt.timedelta(days=6 - dt.datetime.today().weekday()))]
    st.dataframe(this_week)

# Filter data within this month
with st.expander("Announce this month"):
    this_month = calendar_list[(calendar_list['reportDate'].dt.month == dt.datetime.today().month) &
                (calendar_list['reportDate'].dt.year == dt.datetime.today().year)]
    st.dataframe(this_month)