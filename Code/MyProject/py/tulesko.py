#Math 
from ast import Num
from _ast import And
print("Hello")
# Floating point representation
print(5/2)
# Integer devision or floor devision
print(5//2)
#power of
print(2**3)
# Modulus or remainder
print(5%2)

print("*****************************String*****************************************************")
#String
print("vikash's laptop")
print('vikash "laptop"')
print('vikash\'s "laptop"') # \ skip meaning of underscore
print(3*'vikash')
print("c:\dev\navin") # \n will go in next line
#Print raw string
print(r"c:\dev\navin") # just it will print as it is

print("*****************************Variable*****************************************************")
#Variable
name="vikasha"
print(name[0]) #print(name[8]) - IndexError: string index out of range
print(name[-1]) # op is h
print(name[1:4]) # substring ika
print(name[1:])  # 1 to last index
print(name[:4])  # first letter to index
print(name[1:400]) # works fine
print(len(name))  # length
print(name.index("a")) # 3

print("*****************************list*****************************************************")
#list
# define from [] squire bracket
nums=[25,12,36,93,12]
print(nums[0])
print(nums[2:])
print(nums[-1]) #last index
nums[0:2]=[7,8]
print(nums)
names=['vikash','ram','rahul']
values=['vikash',5.7,3]
mil=[nums,names] 
print(mil) # can combine two list
#list are mutable
nums.append(88) # add at last
nums.insert(2, 66) # add at index
nums.remove(12) # to remove element by value 
del nums[2] # to remove element by index 
nums.pop(2) # remove based on index
nums.pop # remove last added element
del nums[2:] # method to delete mutiple values , from 2 index delete all
nums.extend([34,65,234,45]) # to add multiple values
min(nums)
max(nums)
sum(nums)

print("*****************************Tuple*****************************************************")
#Tuple
# its immutable but list are mutable , only thats differnce
# define from () small bracket
# We can create tuple when fixed data required, hence iteration is faster than list
# it doent have any method like list to append , extent
tup=(43,6,23)
print(tup[0])


print("*****************************Set*****************************************************")
#Set
#define from {} braces
# used to removes duplicates
#  It doenst maintail order while retriving
s={34,566,2,567,78,87,2}

print(s) #  It doenst  maintail order while retriving and duplicate removed
#print(s[0]) # error set dont support indexing

#Python set path in Windows abd help
#set path C:\Users\vikash.kumar\AppData\Local\Programs\Python\Python38-32
#set path C:\Users\vikash.kumar\AppData\Local\Programs\Python\Python38-32\Scripts
# then run python to get shell for python
# type help() in cmd to see all python documentation

print("*****************************More on variable*****************************************************")
#More on variable
a=10
# to use address of any data or variable use id() function
b=a
print(id(a)) #1569966144
print(id(b)) #1569966144
print(id(10)) #1569966144
# Python checks the value check, if its ame then assign map to same address.
a=5
print(id(a)) #1569966064
print(id(b)) #1569966144
#if nothing is poiting to any value then GC concept come in picture
#To know type of variable use type() function
PI=3.14
print(type(PI))

print("*****************************Data type*****************************************************")
#Data type
#None data type is same like null
#numeric data type
a=2
b=3.5
c=4+5j
print(type(a)) #<class 'int'>
print(type(b)) #<class 'float'>
print(type(c)) #<class 'complex'>

print("****************************type conversion****************************************************")
#type conversion
d=float(a) # convert int to float
k=complex(a,b) # convert complex data type
print(type(d)) 
print(d)
print(type(k))
print(k)
bool= a>b
print(bool)
print(int(True))
# in python no char data type only string u can use in single code but type will be string only
lst=[34,5,34]
s={34,5,35,4} 
t=(4,45,34,4)
str='r'
print(type(lst)) 
print(type(s)) 
print(type(t)) 
print(type(str))

print("*****************************Range*****************************************************")
#Range
print(range(10)) 
print(type(range(10))) 
print(list(range(10))) # to print range using list [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(list(range(2,10,2))) # print enen numvet range from 2 to 10 differnce is 2  [2, 4, 6, 8]

print("*****************************dictinary*****************************************************")
#dictinary 
d={"vikash":"iphone","rahul":"samsung","soahn":"mi"} # syntax is same as set because key should be unique
print(d.keys())
print(d.values())
print(d.get('vikash')) #iphone
print(d['vikash'])  #iphone can use any way
d["ram"]:["th"] # add value in dicstionanry
d.update({"vikash":"iphone","rahul":"samsung"}) # add multiple value in dictionary
del d["vikash"] # deledte a value 

print("*****************************operators*****************************************************")
#operators
#assignment operators
x=4
a,b=7,8
print(a) #7 
print(b) #8
#Unary operator
n=7
n=-n
print(n)
#relational operator
print(a>b)
#logical operator
print(a>b and a>c)
x=True
x=not x
print(x)

#Number system convertion
print(bin(25))
print(oct(10))
print(hex(16)) #0x10
print(0x10) #16

#BitWise Operators
print(~12) #complement of 12
print(12 & 13) #bitwise and
print(12 | 13) #bitwise or
print(12 ^ 1 ) # Xor two differnr number then 1 else o
print(10 << 2) #left shift

print("*****************************Math Function *****************************************************")
#Important Math Function in Python
import math #need to import
print(math.sqrt(25))
print(math.floor(2.9)) #least value
print(math.ceil(2.4)) #highest integer
print(math.pow(2, 3))
print(math.pi)
print(math.e)
import math as m # we can alias any import library
print(m.pi)
from math import pow,sqrt # we can import only useful function also, then directly we can use
print(pow(2, 3)) 

#Working with PyCharm | 
#python filename.py to run python python

#User input in Python | Command line inputx
#exaple of user input
#a=int(input("enter 1st value")) # use input function, int for change str to int
#b=int(input("enter 2nd value"))
print(a+b)
#example of comand line inpur
import sys
#a=int(sys.argv[1]) # use input function, int for change str to int
#b=int(sys.argv[1])
print(a+b)
# run on command python mycode.py 6 2

print("*****************************Conditinal operator*****************************************************")
# if..elif..else Statement 
x=5
if x==5:
    print("1") #indentation need to use by default 4 spaces or one tab, for multiple line inside if indentation shuld same
elif x==2:
    print("2")
else:
    print("3")
 
print("*****************************Loops*****************************************************")   
#While loop in Pytho
i=3
while i<2:
    print("hi")
    i=i+1
    
#For loop in Python
a=[2,5]
y="vikash" # we can use for llop to iterate list, tupple, set , string 
for ik in y:
    print(ik)
for ik in a:
    print(ik)
for s in [55,33]:
    print(s)
for a in range(10):
    print(a)
for a in range(20,10,-1): # print in reviseerd order
    print(a)
    
#Break Continue Pass 
for a in range(10):
    if a%2==0:
        pass    # breank continiue same it is , pass to use if u dont want to keep ant lines of code
    else:
        print(i)  
    print(a)
    
#Printing Patterns
for i in range(4):
    for j in range(4):
        print("# ",end="")
        
    print()
 
print("*****************************Object Oriented Programming*****************************************************")   
# Object Oriented Programming
#everthing is object in python
class Computer:
    def config(self):
        print("16gb","500mb")
# create obj
comp1=Computer()
comp2=Computer()
# 1st way of calling method
Computer.config(comp1)
Computer.config(comp2)
# 1st way of calling method and most usseful
comp1.config() # comp1 istance is getting paased in self paramter behind the scene
comp2.config()

#_INIT_METHOD 

# Udemy python
#Anaconda is distribution of python
#Jupyter is dev tool and ide for python
#c:/> jupyter notebook  -launch jupyter from cmd

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# List comprihension
x=[1,2,3,4]
out=[]
for num in x:
    out.append(num*2)
print(out)
#or
[num*2 for num in x ] # [(what do u want) for (what) in (complete array)]

# lamda expression
# Map = mapping a function to every element in a sequence
def func(var):
    return var*2
a=func(2)
print(a) #4
sequence=[1,2,3,4,5]
map(func,sequence) #map(function,values) #<map at 0x23c0cd63388>
list(map(func,sequence)) #[2, 4, 6, 8, 10]
#OR
#usually we dont call a def from map function instead of that directly write lamda function in map because of that lamda function caoms in to picture
a= lambda var:var*2
a(2) #4
list(map(lambda var:var*2,sequence))  #[2, 4, 6, 8, 10] # map takees lamda expn or function and call the seq one by one

# filter = filter a function to every element in a sequence
filter(lambda num:num%2==0, sequence) # filter takes lamda or function and for each values from sequnce its checks boolean chack if true then its return that values
list(filter(lambda num:num%2==0, sequence)) #[2, 4]

#Pop
x=[1,2,3,4]
c=x.pop() #4
print(c)
d=x.pop(0) #1
print(d)
'x' in [1,2,3] #fasle
'x' in ['x','y','z'] #true

x=[(1,2),(3,4),(5,6)]
for item in x:
    print(item)
for a,b in x:
    print(b)
    
    
import pandas as pd

df = pd.read_excel('test.xlsx')
print(df.head(5))





