#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[3]:


green_tripdata_df = pd.read_parquet('green_tripdata_2025-11.parquet')
taxi_zone_df = pd.read_csv('taxi_zone_lookup.csv')


# In[6]:


green_tripdata_df.head()


# In[8]:


green_tripdata_df.info()


# In[9]:


taxi_zone_df.info()


# In[10]:


green_tripdata_df.size


# In[11]:


taxi_zone_df.size

