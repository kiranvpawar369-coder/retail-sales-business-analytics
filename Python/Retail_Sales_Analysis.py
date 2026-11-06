#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import required libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("Retail Sales Analytics Project Started!")
print("All libraries imported successfully!")


# In[2]:


# Load the retail sales dataset

df = pd.read_csv("../Dataset/superstore.csv")

print("Dataset loaded successfully!")


# In[3]:


import pandas as pd

# Load dataset using complete file path

file_path = r"D:\Retail-Sales-Business-Analytics\Dataset\superstore.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")


# In[4]:


import os

# Check whether the project folder exists
project_path = r"D:\Retail-Sales-Business-Analytics"

print("Project folder exists:", os.path.exists(project_path))

# Check Dataset folder
dataset_path = os.path.join(project_path, "Dataset")

print("Dataset folder exists:", os.path.exists(dataset_path))

# Display all files inside Dataset
if os.path.exists(dataset_path):
    print("Files inside Dataset:")
    print(os.listdir(dataset_path))


# In[5]:


import pandas as pd

file_path = r"D:\Retail-Sales-Business-Analytics\Dataset\superstore.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")


# In[6]:


import os

dataset_path = r"D:\Retail-Sales-Business-Analytics\Dataset"

print(os.listdir(dataset_path))


# In[7]:


import os

dataset_path = r"D:\Retail-Sales-Business-Analytics\Dataset"

print(os.listdir(dataset_path))


# In[8]:


import pandas as pd

file_path = r"D:\Retail-Sales-Business-Analytics\Dataset\superstore.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Dataset Shape:", df.shape)


# In[9]:


import pandas as pd

# Dataset location
file_path = r"D:\Retail-Sales-Business-Analytics\Dataset\superstore.csv"

# Load dataset with compatible encoding
df = pd.read_csv(file_path, encoding="latin-1")

print("Dataset loaded successfully!")
print("Dataset Shape:", df.shape)


# In[10]:


df.head()


# In[11]:


df.tail()


# In[12]:


df.info()


# In[13]:


# DAY 2: DATA CLEANING

print("Starting Data Cleaning Process")
print("--------------------------------")

print("Original Dataset Shape:", df.shape)


# In[14]:


missing_values = df.isnull().sum()

print("Missing Values in Each Column:")
print(missing_values[missing_values > 0])


# In[15]:


duplicate_count = df.duplicated().sum()

print("Total Duplicate Records:", duplicate_count)


# In[16]:


df['Order Date'] = pd.to_datetime(
    df['Order Date'],
    errors='coerce'
)

df['Ship Date'] = pd.to_datetime(
    df['Ship Date'],
    errors='coerce'
)

print(df[['Order Date', 'Ship Date']].dtypes)


# In[17]:


print(df.dtypes)


# In[18]:


print(df.isnull().sum())


# In[19]:


import pandas as pd
import numpy as np

# Reload original dataset
file_path = r"D:\Retail-Sales-Business-Analytics\Dataset\superstore.csv"

df = pd.read_csv(file_path, encoding="latin-1")

# Remove exact duplicate rows
df = df.drop_duplicates()

# Convert date columns
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')

# Convert numerical columns
numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit']

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Handle missing values
df = df.dropna(subset=['Order Date', 'Ship Date', 'Sales', 'Profit'])

# Save cleaned dataset
cleaned_path = r"D:\Retail-Sales-Business-Analytics\Dataset\superstore_cleaned.csv"

df.to_csv(cleaned_path, index=False)

print("DATA CLEANING COMPLETED!")
print("Final Dataset Shape:", df.shape)
print("Missing Values:", df.isnull().sum().sum())


# In[20]:


total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()
total_quantity = df['Quantity'].sum()

profit_margin = (total_profit / total_sales) * 100

print("Total Sales:", round(total_sales, 2))
print("Total Profit:", round(total_profit, 2))
print("Total Orders:", total_orders)
print("Total Quantity:", total_quantity)
print("Profit Margin:", round(profit_margin, 2), "%")


# In[21]:


excel_path = r"D:\Retail-Sales-Business-Analytics\Dataset\superstore_cleaned.xlsx"

df.to_excel(excel_path, index=False)

print("Excel file exported successfully!")


# In[ ]:




