# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 14:09:23 2018

@author: Admin
"""
# Loading the required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sns
import datetime as dt
import calendar 
from scipy.stats import skew,kurtosis

import warnings
warnings.filterwarnings('ignore')

#from subprocess import check_output
#print(check_output(["ls","-l"]).splitlines()
## scritto cosi' non funziona, nel caso controllare la sintassi di check_output

# questa e' l'alternativa per stampare l'elenco dei file nella cartella olist_data
import os 
files = os.listdir('../olist_data')
for file in files:
    print(file)
    

## Reading the datas:
customer=pd.read_csv("../olist_data/olist_customers_dataset.csv")  ### Unique customer id 
geo=pd.read_csv("../olist_data/olist_geolocation_dataset.csv")  ## Location data
order = pd.read_csv("../olist_data/olist_orders_dataset.csv")  ## Unclassified orders dataset
items = pd.read_csv("../olist_data/olist_order_items_dataset.csv") ## items dataset
payment = pd.read_csv("../olist_data/olist_order_payments_dataset.csv")  ### Payment dataset
review = pd.read_csv("../olist_data/olist_order_reviews_dataset.csv") ## review dataset
sellers=pd.read_csv("../olist_data/olist_sellers_dataset.csv") ## Seller information
translation = pd.read_csv("../olist_data/product_category_name_translation.csv")  ## Product translation to english
product = pd.read_csv("../olist_data/olist_products_dataset.csv")

customer.shape
geo.shape
order.shape
items.shape
payment.shape
review.shape
sellers.shape
translation.shape
product.shape

## Joining the order and payment
order_pay = pd.merge(order, payment, how="left", on=['order_id','order_id'])

## Joining the order_pay with product category translation
order_product = pd.merge(order_pay, items, how="left", on=['order_id','order_id'])
order_product = pd.merge(order_product, product, how="left", on=['product_id','product_id'])

## Order Summary
print("Total number of orders in the database:", order['order_id'].nunique())
print("Total number of customers:", order['customer_id'].nunique())

## Check the order status
status = order.groupby('order_status')['order_id'].nunique().sort_values(ascending=False)
status

## Order value summary
print("Maximum order amount is BRL:",order_product['price'].max())
print("Minimum order amount is BRL:",order_product['price'].min())
print("Average order amount is BRL:",order_product['price'].mean())
print("Median order amount is BRL:",order_product['price'].median())

## We summarize the order with the help of the order id and have a look at the price and freight value
value = order_product.groupby('order_id')['price','freight_value'].sum().sort_values(by='price',ascending=False).reset_index()
value.head()

order_product = order_product[np.isfinite(order_product['price'])]

## Lets plot a histogram of the price and freight value to understend the skewness of the data
plt.figure(figsize=(12,10))

plt.subplot(221)
g = sns.distplot(np.log(order_product['price'] + 1))
g.set_title("Price of Orders - Distribution", fontsize=15)
g.set_xlabel("")
g.set_ylabel("Frequency", fontsize=12)

plt.subplot(222)
g1 = sns.distplot(np.log(order_product['freight_value'] + 1))
g1.set_title("Freight Value of Orders - Distribution", fontsize=15)
g1.set_xlabel("")
g1.set_ylabel("Frequency", fontsize=12)

print("Skewness of the transaction value:",skew(np.log(order_product['price']+1)))
print("Excess Kurtosis of the transaction value:",kurtosis(np.log(order_product['price']+1)))

## NB: order_usual=order.groupby('order_id')['order_items_qty'].aggregate('sum').reset_index()

## Number of products people ususally order
order_usual=order_product.groupby('order_id')['order_item_id'].aggregate('sum').reset_index()
order_usual=order_usual['order_item_id'].value_counts()
order_usual.head()

plt.figure(figsize=(6,6))
ax=sns.barplot(x=order_usual.index,y=order_usual.values,color="green")
ax.set_xlabel("Number of products added in order")
ax.set_ylabel("Number of orders")
ax.set_title("Number of products people usually order")
ax.set_xticklabels(ax.get_xticklabels(),rotation=90)

## Most bought product category
order_product.shape
order_product = pd.merge(order_product,translation,on='product_category_name',how='left')
order_product.shape

most_product = order_product.groupby('product_category_name_english').aggregate({'order_id':'count'}).rename(columns={'order_id':'order_count'}).sort_values(by='order_count',ascending=False).reset_index()
most_product.head()

## Visualizing top 10 most bought product categories
plt.figure(figsize=(6,6))
sns.barplot(x='product_category_name_english',y='order_count',data=most_product[:10],color='blue')
plt.xlabel("Product Category")
plt.ylabel("Total Number of orders")
plt.title("Most bought product categories")
plt.xticks(rotation='vertical')
plt.show()

## Order Trend
order_product['order_purchase_timestamp']=pd.to_datetime(order_product['order_purchase_timestamp'])
order_product['order_delivered_customer_date']=pd.to_datetime(order_product['order_delivered_customer_date'])

# create new columns for date, day, time, month
order_product['weekday']=order_product['order_purchase_timestamp'].dt.weekday_name 
order_product['year']=order_product['order_purchase_timestamp'].dt.year
order_product['monthday']=order_product['order_purchase_timestamp'].dt.day
order_product['weekday']=order_product['order_purchase_timestamp'].dt.weekday 
order_product['month']=order_product['order_purchase_timestamp'].dt.month 
order_product['hour']=order_product['order_purchase_timestamp'].dt.hour










