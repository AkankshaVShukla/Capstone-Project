import pandas as pd
import matplotlib
import numpy as np
import datetime as dt
import csv
from datetime import datetime

#Loading Calendar Data
calendar_data=pd.read_csv('../Data/calendar.csv',sep=',')
print(calendar_data.head())

#########Data Cleaning################
#Removing rows where prices are null and removing $ from price
calendar_data=calendar_data.dropna()
calendar_data['price']=calendar_data['price'].str.replace('$','')
print(calendar_data.head())

#########Data Exploration#############
calendar_data['price']=pd.to_numeric(calendar_data['price'],errors='coerce')
calendar_data['weekday']=pd.to_datetime(calendar_data['date']).dt.dayofweek
print(calendar_data.head())


avg_price=[]
for i in calendar_data['date'].unique():
    avg_price.append(calendar_data[calendar_data['date'] == i]['price'].mean())


df = pd.DataFrame({'price':avg_price})
df.to_csv("daily_price.csv",index=False)

########################################
weekDays=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

price_data=dict.fromkeys(weekDays)
for i in price_data:
    price_data[i]=[]

listing_id=[]
for i in calendar_data['listing_id'].unique():
    listing_id.append(i)
    for j,k in enumerate(weekDays):
        weekday=calendar_data['weekday'] == j
        listing=calendar_data['listing_id'] == i
        price_data[k].append(calendar_data[weekday & listing]['price'].mean())

df = pd.DataFrame(price_data)
df['listing_id'] = listing_id
df = df[['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'listing_id']]

for i in weekDays[0:6]:
    df[i] = df[i]/df['Sun']
df['Sun']= 1


result = dict.fromkeys(weekDays)
for index,i in enumerate(result):
    result[i]=df.mean()[i]
print(result)

#{'Wed': 0.99303064410570607, 'Sun': 1.0, 'Fri': 1.029393190209331, 'Tue': 0.99245980467384853, 'Mon': 0.99546177387912238, 'Thu': 0.99879807138242516, 'Sat': 1.031146576455956}
#Taking Sunday as base, we can say that price on Friday and Saturday is higher from the above result.
