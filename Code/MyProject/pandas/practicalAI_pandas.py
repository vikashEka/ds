#!/usr/bin/env python
# coding: utf-8

# # Pandas

# <img src="https://raw.githubusercontent.com/GokuMohandas/practicalAI/master/images/logo.png" width=150>
# 
# In this notebook, we'll learn the basics of data analysis with the Python Pandas library.
# 
# <img src="https://raw.githubusercontent.com/GokuMohandas/practicalAI/master/images/pandas.png" width=500>
# 
# 
# 

# # Uploading the data

# We're first going to get some data to play with. We're going to load the titanic dataset from the public link below.

# In[ ]:


import urllib


# In[ ]:


# Upload data from GitHub to notebook's local drive
url = "https://raw.githubusercontent.com/GokuMohandas/practicalAI/master/data/titanic.csv"
response = urllib.request.urlopen(url)
html = response.read()
with open('titanic.csv', 'wb') as f:
    f.write(html)


# In[ ]:


# Checking if the data was uploaded
get_ipython().system('ls -l ')


# # Loading the data

# Now that we have some data to play with, let's load it into a Pandas dataframe. Pandas is a great Python library for data analysis.

# In[ ]:


import pandas as pd


# In[ ]:


# Read from CSV to Pandas DataFrame
df = pd.read_csv("titanic.csv", header=0)


# In[ ]:


# First five items
df.head()


# These are the diferent features: 
# * pclass: class of travel
# * name: full name of the passenger
# * sex: gender
# * age: numerical age
# * sibsp: # of siblings/spouse aboard
# * parch: number of parents/child aboard
# * ticket: ticket number
# * fare: cost of the ticket
# * cabin: location of room
# * emarked: port that the passenger embarked at (C - Cherbourg, S - Southampton, Q = Queenstown)
# * survived: survial metric (0 - died, 1 - survived)

# # Exploratory analysis

# We're going to use the Pandas library and see how we can explore and process our data.

# In[ ]:


# Describe features
df.describe()


# In[ ]:


# Histograms
df["age"].hist()


# In[ ]:


# Unique values
df["embarked"].unique()


# In[ ]:


# Selecting data by feature
df["name"].head()


# In[ ]:


# Filtering
df[df["sex"]=="female"].head() # only the female data appear


# In[ ]:


# Sorting
df.sort_values("age", ascending=False).head()


# In[ ]:


# Grouping
survived_group = df.groupby("survived")
survived_group.mean()


# In[ ]:


# Selecting row
df.iloc[0, :] # iloc gets rows (or columns) at particular positions in the index (so it only takes integers)


# In[ ]:


# Selecting specific value
df.iloc[0, 1]


# In[ ]:


# Selecting by index
df.loc[0] # loc gets rows (or columns) with particular labels from the index


# # Preprocessing

# In[ ]:


# Rows with at least one NaN value
df[pd.isnull(df).any(axis=1)].head()


# In[ ]:


# Drop rows with Nan values
df = df.dropna() # removes rows with any NaN values
df = df.reset_index() # reset's row indexes in case any rows were dropped
df.head()


# In[ ]:


# Dropping multiple columns
df = df.drop(["name", "cabin", "ticket"], axis=1) # we won't use text features for our initial basic models
df.head()


# In[ ]:


# Map feature values
df['sex'] = df['sex'].map( {'female': 0, 'male': 1} ).astype(int)
df["embarked"] = df['embarked'].dropna().map( {'S':0, 'C':1, 'Q':2} ).astype(int)
df.head()


# # Feature engineering

# In[ ]:


# Lambda expressions to create new features
def get_family_size(sibsp, parch):
    family_size = sibsp + parch
    return family_size

df["family_size"] = df[["sibsp", "parch"]].apply(lambda x: get_family_size(x["sibsp"], x["parch"]), axis=1)
df.head()


# In[ ]:


# Reorganize headers
df = df[['pclass', 'sex', 'age', 'sibsp', 'parch', 'family_size', 'fare', 'embarked', 'survived']]
df.head()


# # Saving data

# In[ ]:


# Saving dataframe to CSV
df.to_csv("processed_titanic.csv", index=False)


# In[ ]:


# See your saved file
get_ipython().system('ls -l')

