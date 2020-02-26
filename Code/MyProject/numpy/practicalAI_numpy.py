#!/usr/bin/env python
# coding: utf-8

# # NumPy

# <img src="https://raw.githubusercontent.com/GokuMohandas/practicalAI/master/images/logo.png" width=150>
# 
# In this lesson we will learn the basics of numerical analysis using the NumPy package.
# 
# <img src="https://raw.githubusercontent.com/GokuMohandas/practicalAI/master/images/numpy.png" width=300>
# 
# 
# 

# # NumPy basics

# In[ ]:


import numpy as np


# In[ ]:


# Set seed for reproducibility
np.random.seed(seed=1234)


# In[3]:


# Scalars
x = np.array(6) # scalar
print ("x: ", x)
# Number of dimensions
print ("x ndim: ", x.ndim)
# Dimensions
print ("x shape:", x.shape)
# Size of elements
print ("x size: ", x.size)
# Data type
print ("x dtype: ", x.dtype)


# In[4]:


# 1-D Array
x = np.array([1.3 , 2.2 , 1.7])
print ("x: ", x)
print ("x ndim: ", x.ndim)
print ("x shape:", x.shape)
print ("x size: ", x.size)
print ("x dtype: ", x.dtype) # notice the float datatype


# In[6]:


# 3-D array (matrix)
x = np.array([[[1,2,3], [4,5,6], [7,8,9]]])
print ("x:\n", x)
print ("x ndim: ", x.ndim)
print ("x shape:", x.shape)
print ("x size: ", x.size)
print ("x dtype: ", x.dtype)


# In[7]:


# Functions
print ("np.zeros((2,2)):\n", np.zeros((2,2)))
print ("np.ones((2,2)):\n", np.ones((2,2)))
print ("np.eye((2)):\n", np.eye((2)))
print ("np.random.random((2,2)):\n", np.random.random((2,2)))


# # Indexing

# In[8]:


# Indexing
x = np.array([1, 2, 3])
print ("x[0]: ", x[0])
x[0] = 0
print ("x: ", x)


# In[9]:


# Slicing
x = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])
print (x)
print ("x column 1: ", x[:, 1]) 
print ("x row 0: ", x[0, :]) 
print ("x rows 0,1,2 & cols 1,2: \n", x[:3, 1:3]) 


# In[10]:


# Integer array indexing
print (x)
rows_to_get = np.arange(len(x))
print ("rows_to_get: ", rows_to_get)
print(rows_to_get)
cols_to_get = np.array([0, 2, 1])
print ("cols_to_get: ", cols_to_get)
print ("indexed values: ", x[rows_to_get, cols_to_get])


# In[11]:


# Boolean array indexing
x = np.array([[1,2], [3, 4], [5, 6]])
print ("x:\n", x)
print ("x > 2:\n", x > 2)
print ("x[x > 2]:\n", x[x > 2])


# # Array math

# In[12]:


# Basic math
x = np.array([[1,2], [3,4]], dtype=np.float64)
y = np.array([[1,2], [3,4]], dtype=np.float64)
print ("x + y:\n", np.add(x, y)) # or x + y
print ("x - y:\n", np.subtract(x, y)) # or x - y
print ("x * y:\n", np.multiply(x, y)) # or x * y


# <img src="https://raw.githubusercontent.com/GokuMohandas/practicalAI/master/images/matrix.png" width=400>
# 

# In[13]:


# Dot product
a = np.array([[1,2,3], [4,5,6]], dtype=np.float64) # we can specify dtype
b = np.array([[7,8], [9,10], [11, 12]], dtype=np.float64)
print (a.dot(b))


# In[14]:


# Sum across a dimension
x = np.array([[1,2],[3,4]])
print (x)
print ("sum all: ", np.sum(x)) # adds all elements
print ("sum by col: ", np.sum(x, axis=0)) # add numbers in each column
print ("sum by row: ", np.sum(x, axis=1)) # add numbers in each row


# In[15]:


# Transposing
print ("x:\n", x)
print ("x.T:\n", x.T)


# # Advanced

# In[16]:


# Tile
x = np.array([[1,2], [3,4]])
y = np.array([5, 6])
addent = np.tile(y, (len(x), 1))
print ("addent: \n", addent)
z = x + addent
print ("z:\n", z)


# In[17]:


# Broadcasting
x = np.array([[1,2], [3,4]])
y = np.array([5, 6])
z = x + y
print ("z:\n", z)


# In[18]:


# Reshaping
x = np.array([[1,2], [3,4], [5,6]])
print (x)
print ("x.shape: ", x.shape)
y = np.reshape(x, (2, 3))
print ("y.shape: ", y.shape)
print ("y: \n", y)


# In[19]:


# Removing dimensions
x = np.array([[[1,2,1]],[[2,2,3]]])
print ("x.shape: ", x.shape)
y = np.squeeze(x, 1) # squeeze dim 1
print ("y.shape: ", y.shape) 
print ("y: \n", y)


# In[20]:


# Adding dimensions
x = np.array([[1,2,1],[2,2,3]])
print ("x.shape: ", x.shape)
y = np.expand_dims(x, 1) # expand dim 1
print ("y.shape: ", y.shape) 
print ("y: \n", y)


# # Additional resources

# You don't have to memorize anything here and we will be taking a closer look at NumPy in the later lessons. If you are curious about more checkout the [NumPy reference manual](https://docs.scipy.org/doc/numpy-1.15.1/reference/).
