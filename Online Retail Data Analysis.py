#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import warnings
warnings.filterwarnings('ignore')


# In[4]:


df = pd.read_excel("OnlineRetail.xlsx")
df.head()
df1 = df


# In[5]:


df1.Country.nunique()


# In[6]:


df1.Country.unique()


# In[7]:


customer_country=df1[['Country','CustomerID']].drop_duplicates()


# In[8]:


customer_country.groupby(['Country'])['CustomerID'].aggregate('count').reset_index().sort_values('CustomerID', ascending=False)


# In[9]:


df1 = df1.loc[df1['Country'] == 'United Kingdom']


# In[10]:


df1.isnull().sum(axis=0)


# In[11]:


df1 = df1[pd.notnull(df1['CustomerID'])]


# In[12]:


df1.Quantity.min()


# In[13]:


df1 = df1[(df1['Quantity']>0)]
df1.shape
df1.info()


# In[14]:


def unique_counts(df1):
   for i in df1.columns:
       count = df1[i].nunique()
       print(i, ": ", count)
unique_counts(df1)


# In[15]:


df1['TotalPrice'] = df1['Quantity'] * df1['UnitPrice']


# In[16]:


df1['InvoiceDate'].max()


# In[17]:


import datetime as dt
NOW = dt.datetime(2011,12,10)
df1['InvoiceDate'] = pd.to_datetime(df1['InvoiceDate'])


# In[18]:


rfmTable = df1.groupby('CustomerID').agg({'InvoiceDate': lambda x: (NOW - x.max()).days, 'InvoiceNo': lambda x: len(x), 'TotalPrice': lambda x: x.sum()})
rfmTable['InvoiceDate'] = rfmTable['InvoiceDate'].astype(int)
rfmTable.rename(columns={'InvoiceDate': 'recency', 
                         'InvoiceNo': 'frequency', 
                         'TotalPrice': 'monetary_value'}, inplace=True)


# In[19]:


rfmTable.head()


# In[24]:


first_customer = df1[df1['CustomerID']== 123456.0]
first_customer


# In[25]:


quantiles = rfmTable.quantile(q=[0.25,0.5,0.75])
quantiles = quantiles.to_dict()


# In[26]:


segmented_rfm = rfmTable


# In[27]:


def RScore(x,p,d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]: 
        return 3
    else:
        return 4
    
def FMScore(x,p,d):
    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.50]:
        return 3
    elif x <= d[p][0.75]: 
        return 2
    else:
        return 1


# In[28]:


segmented_rfm['r_quartile'] = segmented_rfm['recency'].apply(RScore, args=('recency',quantiles,))
segmented_rfm['f_quartile'] = segmented_rfm['frequency'].apply(FMScore, args=('frequency',quantiles,))
segmented_rfm['m_quartile'] = segmented_rfm['monetary_value'].apply(FMScore, args=('monetary_value',quantiles,))
segmented_rfm.head()


# In[35]:


segmented_rfm['RFMScore'] = segmented_rfm.r_quartile.map(str) + segmented_rfm.f_quartile.map(str) + segmented_rfm.m_quartile.map(str)
segmented_rfm.head()


# In[36]:


segmented_rfm[segmented_rfm['RFMScore']=='111'].sort_values('monetary_value', ascending=False).head(10)


# In[37]:


segmented_rfm[segmented_rfm['RFMScore']=='111'].sort_values('frequency', ascending=False).head(10)


# In[38]:


segmented_rfm[segmented_rfm['RFMScore']=='111'].sort_values('recency', ascending=False).head(10)


# In[ ]:




