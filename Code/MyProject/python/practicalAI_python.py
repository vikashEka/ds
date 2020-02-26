#!/usr/bin/env python
# coding: utf-8

# # Introduction to Python

# <img src="https://raw.githubusercontent.com/GokuMohandas/practicalAI/master/images/logo.png" width=150>
# 
# In this lesson we will learn the basics of the Python programming language (version 3). We won't learn everything about Python but enough to do some basic machine learning.
# 
# <img src="https://raw.githubusercontent.com/GokuMohandas/practicalAI/master/images/python.png" width=350>
# 
# 
# 

# #  Variables

# Variables are objects in Python that can hold anything with numbers or text. Let's look at how to create some variables.

# In[1]:


# Numerical example
x = 6
print (x)


# In[2]:


# Text example
x = "hello dd"
print (x)


# In[ ]:


# Variables can be used with each other
a = 1
b = 2
c = a + b
print (c)


# Variables can come in lots of different types. Even within numerical variables, you can have integers (int), floats (float), etc. All text based variables are of type string (str). We can see what type a variable is by printing its type.

# In[ ]:


# int variable
x = 5
print (x)
print (type(x))

# float variable
x = 5.0
print (x)
print (type(x))

# text variable
x = "5" 
print (x)
print (type(x))

# boolean variable
x = True
print (x)
print (type(x))


# It's good practice to know what types your variables are. When you want to use numerical operations on them, they need to be compatible. 

# In[ ]:


# int variables
a = 5
b = 3
print (a + b)

# string variables
a = "5"
b = "3"
print (a + b)


# #  Lists

# Lists are objects in Python that can hold a ordered sequence of numbers **and** text.

# In[ ]:


# Creating a list
list_x = [3, "hello", 1]
print (list_x)


# 

# In[ ]:


# Adding to a list
list_x.append(7)
print (list_x)


# In[ ]:


# Accessing items at specific location in a list
print ("list_x[0]: ", list_x[0])
print ("list_x[1]: ", list_x[1])
print ("list_x[2]: ", list_x[2])
print ("list_x[-1]: ", list_x[-1]) # the last item
print ("list_x[-2]: ", list_x[-2]) # the second to last item


# In[ ]:


# Slicing
print ("list_x[:]: ", list_x[:])
print ("list_x[2:]: ", list_x[2:])
print ("list_x[1:3]: ", list_x[1:3])
print ("list_x[:-1]: ", list_x[:-1])


# In[ ]:


# Length of a list
len(list_x)


# In[ ]:


# Replacing items in a list
list_x[1] = "hi"
print (list_x)


# In[ ]:


# Combining lists
list_y = [2.4, "world"]
list_z = list_x + list_y
print (list_z)


# # Tuples

# Tuples are also objects in Python that can hold data but you cannot replace their values (for this reason, tuples are called immutable, whereas lists are known as mutable).

# In[ ]:


# Creating a tuple
tuple_x = (3.0, "hello")
print (tuple_x)


# In[ ]:


# Adding values to a tuple
tuple_x = tuple_x + (5.6,)
#print (tuple_x)


# In[ ]:


# Trying to change a tuples value (you can't)
#tuple_x[1] = "world"


# # Dictionaries

# Dictionaries are Python objects that hold key-value pairs. In the example dictionary below, the keys are the "name" and "eye_color" variables. They each have a value associated with them. A dictionary cannot have two of the same keys. 

# In[ ]:


# Creating a dictionary
goku = {"name": "Goku",
        "eye_color": "brown"}
print (goku)
print (goku["name"])
print (goku["eye_color"])


# In[ ]:


# Changing the value for a key
goku["eye_color"] = "green"
print (goku)


# In[ ]:


# Adding new key-value pairs
goku["age"] = 24
print (goku)


# In[ ]:


# Length of a dictionary
print (len(goku))


# # If statements

# You can use `if` statements to conditionally do something.

# In[ ]:


# If statement
x = 4
if x < 1:
    score = "low"
elif x <= 4:
    score = "medium"
else:
    score = "high"
print (score)


# In[ ]:


# If statment with a boolean
x = True
if x:
    print ("it worked")


# # Loops

# In Python, you can use `for` loop to iterate over the elements of a sequence such as a list or tuple, or use `while` loop to do something repeatedly as long as a condition holds.

# In[ ]:


# For loop
x = 1
for i in range(3): # goes from i=0 to i=2
    x += 1 # same as x = x + 1
    print ("i={0}, x={1}".format(i, x)) # printing with multiple variables


# In[ ]:


# Loop through items in a list
x = 1
for i in [0, 1, 2]:
    x += 1
    print ("i={0}, x={1}".format(i, x))


# In[ ]:


# While loop
x = 3
while x > 0:
    x -= 1 # same as x = x - 1
    print (x)


# # Functions

# Functions are a way to modularize reusable pieces of code. 

# In[ ]:


# Create a function
def add_two(x):
    x += 2
    return x

# Use the function
score = 0
score = add_two(x=score)
print (score)


# In[ ]:


# Function with multiple inputs
def join_name(first_name, last_name):
    joined_name = first_name + " " + last_name
    return joined_name

# Use the function
first_name = "Goku"
last_name = "Mohandas"
joined_name = join_name(first_name=first_name, last_name=last_name)
print (joined_name)


# # Classes

# Classes are a fundamental piece of object oriented programming in Python.

# In[ ]:


# Creating the class
class Pets(object):
  
    # Initialize the class
    def __init__(self, species, color, name):
        self.species = species
        self.color = color
        self.name = name

    # For printing  
    def __str__(self):
        return "{0} {1} named {2}.".format(self.color, self.species, self.name)

    # Example function
    def change_name(self, new_name):
        self.name = new_name


# In[ ]:


# Creating an instance of a class
my_dog = Pets(species="dog", color="orange", name="Guiness",)
print (my_dog)
print (my_dog.name)


# In[ ]:


# Using a class's function
my_dog.change_name(new_name="Charlie")
print (my_dog)
print (my_dog.name)


# # Additional resources

# This was a very quick look at Python and we'll be learning more in future lessons. If you want to learn more right now before diving into machine learning, check out this free course: [Free Python Course](https://www.codecademy.com/learn/learn-python)
