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
files = os.listdir('./olist_data')
for file in files:
    print(file)
    

## Reading the datas:
customer=pd.read_csv("./olist_data/olist_customers_dataset.csv")  ### Unique customer id 
geo=pd.read_csv("./olist_data/olist_geolocation_dataset.csv")  ## Location data
order = pd.read_csv("./olist_data/olist_orders_dataset.csv")  ## Unclassified orders dataset
items = pd.read_csv("./olist_data/olist_order_items_dataset.csv") ## items dataset
payment = pd.read_csv("./olist_data/olist_order_payments_dataset.csv")  ### Payment dataset
review = pd.read_csv("./olist_data/olist_order_reviews_dataset.csv") ## review dataset
sellers=pd.read_csv("./olist_data/olist_sellers_dataset.csv") ## Seller information
product = pd.read_csv("./olist_data/product_category_name_translation.csv")  ## Product translation to english

customer.shape
geo.shape
order.shape
items.shape
payment.shape
review.shape
sellers.shape
product.shape

## Joining the order and payment
order_pay = pd.merge(order, payment, how="left", on=['order_id','order_id'])

## Joining the order_pay with product category translation
order_product = pd.merge(order_pay, product, how="left", on=['product_category_name','product_category_name'])
