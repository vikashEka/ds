# python are case sensative
# a=5,A=5 both are diffrent
# variable name cnt start with speacial che except _ underscore.
# generics not suppported in pyton
# python dont have data type of char, it treated as string
# from Operator.Airthmatic import addition -> here OPerator is packge, Aithmatic is module and addition is method => use addition(3,5)
# from Operator import Airthmatice =>use  Airthmatic.addition(4,6)
# hierarvhy- method=>module=>package

# install pandas
# pip install pandas
# pip install numpy
# Read excel file
import pandas as pd
from unittest.mock import inplace
df = pd.read_excel("test.xlsx")   
# to see top 5 row
print(df.head())
print("++++++++++++++++++++++++++")
# pandas
# can read varity of files 
# can read,write,manupulating of data
# size of data (a,b) based on row and column format
print(df.shape)
# Tosee last five row
print(df.tail())
# bottom 7 row
print(df.tail(7))
# to seee all name of colums
print(df.columns)  # Index(['FirstName', 'Salary', 'PIN', 'AGE', 'location'], dtype='object')
# select column names
print(df['FirstName'])
# seelsect column and with last 3 data , both combinations
print(df['FirstName'].tail(3))
# select multiple colums
print(df[['FirstName', 'Salary']])  # need to pass in 2 array
print("++++++++++++++++++++++++++")
      
# Indexing the data frame
# select row by their positions like limit or rownum
print(df.iloc[:3])  # before : its starting index and after : its end limit
# select row and column column by their positions like limit or rownum
print(df.iloc[:, :2])  # before , its row stating from 0 to complete and after , its column start from 0 to 2
# Index subset or slice -print coloumn filter based on condition
print(df[df['AGE'] == 33])
print("++++++++++++++++++++++++++")
      
# Data Manupulation and visualization
# Sorting data frames
import pandas as pd
df = pd.read_excel("test.xlsx")   
df = df.dropna(how="any")
# to see top 5 row
print(df.head())
# sort by values use sort_values() function
sorted_data=df.sort_values(by='AGE')
print(sorted_data[:5])
# sort by values with multiple options decending and inplace true means it will refelect the data in original df not required assignment
df.sort_values(by='AGE', ascending=False,inplace=True) 
print(df[:5])
# sort by values with multiple sort column 
df.sort_values(by=['Salary','AGE'], ascending=False,inplace=True) # first it will sort based on salary then age
print(df[:10])
# sort by index default created
df.sort_index(inplace=True) # it will re arrande the data frame
print(df)

#Merging data frames
#Concat function
df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
                    'B': ['B0', 'B1', 'B2', 'B3'],
                    'C': ['C0', 'C1', 'C2', 'C3'],
                    'D': ['D0', 'D1', 'D2', 'D3']},
                    index=[0, 1, 2, 3])
df2 = pd.DataFrame({'A': ['A4', 'A5', 'A6', 'A7'],
                    'B': ['B4', 'B5', 'B6', 'B7'],
                    'C': ['C4', 'C5', 'C6', 'C7'],
                    'D': ['D4', 'D5', 'D6', 'D7']},
                    index=[4, 5, 6, 7])
df3=pd.concat([df1,df2])
print(df3)
#concat with recognise combined df labeling
df3=pd.concat([df1,df2],keys=['x','y'])
print(df3)
#fetch lebel df from combined df(get indivisual df)
print(df3.loc['y'])
#From merging df its pending of Data Manupulation and visualization


