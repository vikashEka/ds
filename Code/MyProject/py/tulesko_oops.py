#_INIT_METHOD
from math import fabs
import com
from distutils.log import info
from copyreg import constructor
from select import select
from threading import Thread
class Computer:
    
    def __init__(self):
        print("Hi")

    def config(self):
        print("16gb", "500mb")

comp1 = Computer()
comp2 = Computer()
comp1.config() 
comp2.config()

# on every object call init method will get invoke like constructor
print("==============================================")
class Computer1:
    
    def __init__(self,cpu,ram):
        self.cpu=cpu
        self.ram=ram
        print("Hi")

    def config(self):
        print(self.cpu, self.ram)

comp1 = Computer1("i5","16")
comp2 = Computer1("i3","32")
comp1.config() 
comp2.config()
# example of proper object creation

print("==============================================")
# constructor, self and comparing objects
class Computer2:
    
    def __init__(self,cpu,ram):
        self.cpu=cpu
        self.ram=ram
    
    def update(self):  # using method call change value
        self.cpu="i8"

comp1 = Computer2("i5","16")
comp2 = Computer2("i3","32")
comp3 = Computer2("i5","16")
print(id(comp1))
print(id(comp3)) # memory address value will be aways differnt 
print(comp1.cpu)
print(comp2.cpu)
comp1.cpu="i7"
print(comp1.cpu)
comp1.update()
print(comp1.cpu)

print("==============================================")
# comparing objects
# compare(who is calling, whom to compare)
class Computer3:
    
    def __init__(self,cpu,ram):
        self.cpu=cpu
        self.ram=ram

    def compare(self,comp2): # self is comp1 object and other is other one
        if self.ram== comp2.ram:
            return True
        else:
            return False
        
comp1 = Computer3("i5","16")
comp2 = Computer3("i3","32")
comp3 = Computer3("i5","16")

if comp1.compare(comp3): # comapre is not in build method , we need to implement it
    print("equal")       
else:
    print("not equal")

print("==============================================")
# types of variable
# class variable/static varible - created outside init
# instance/object varibale created inside init

class Computer4:
    wheel=4
    def __init__(self,mil,com):
       self.mil=mil
       self.com=com

comp4 = Computer4("10","BMW")
comp5 = Computer4("10","BMW")
print(comp4.mil)
print(comp4.wheel)
Computer4.wheel=5
print(comp4.wheel)
print(comp5.wheel) # class variable shared to all object, but instance not

print("==============================================") 
#Types of Methods :
class Computer5:
    wheel=4
    def __init__(self,mil,com):
       self.mil=mil
       self.com=com
       # insatnce methods
    def set_mil(self,mil): #mutators
        self.mil=mil
    def get_mil(self): #accessors
        return self.mil
    # class methods
    @classmethod # special decorator required 
    def getWheel(cls): # cls for class var
        return cls.wheel
    # static methods
    @staticmethod
    def info(): # this method nothing to do with classor onstance varivale
        print("inside info")
    
# if u r working with instance var then use self, if working with class var then use cls, if working static then use nothing
comp4 = Computer5("10","BMW")
comp5 = Computer5("10","BMW")
print(comp4.get_mil())
print(Computer5.getWheel())
Computer5.info()

#Inner Class
class Student:
    
    def __init__(self,name,roll):
        self.name=name
        self.roll=roll
        self.lap=self.Laptop()
       
    def show(self):
        print(self.name, self.roll)
        
    class Laptop:
        def __init__(self):
            self.brand="HP" 

s1 = Student("vikash","16")
s1.show() 
print(s1.lap.brand) 
print("================%%%%%%%%%%%%%%%==============================") 
#Inheritance
class A:
    def f1(self):
        print("inside A")
        
class B(A):        #single level
    def f2(self):
        print("inside B")
        
class C(B):       # multiple level C(A,B)
    def f3(self):
        print("inside C")

comp1 = A()
comp2 = B()
comp3 = C()
comp3.f1()

print("==========================================")
#Constructor in inheritance
class A1:
    def __init__(self):
        print("inside A")
        
class B1(A1):      
       pass    
comp1 = B1() # if subclass dont have constructor then only look for super constructor op-inside A
print("==========================================")
class A2:
    def __init__(self):
        print("inside A2")
        
class B2(A2):      
      def __init__(self):
        print("inside B2") 
comp1 = B2()  ## if subclass  have constructor then only caall sub class constructor op-inside B2, its not like java
print("==========================================")
# if u want to call super clas use super() method
#u can use suer method to call init/method
class A3:
    def __init__(self):
        print("inside A3")
        
class B3(A3):      
      def __init__(self):
        super().__init__()  # it will call super call constructor
        print("inside B3") 
comp1 = B3()
print("==========================================")
#MRO(Method resolution order)
class A4:
    def __init__(self):
        print("inside A4")
    def f1(self):
        print("inside A4 method")        
class B4:      
    def __init__(self):
        print("inside B4")
    def f1(self):
        print("inside B4 method")     
class C4(A4,B4):        # in case of multiple inheritace it cal left to right
      def __init__(self):
        super().__init__() #inside A4
        super().f1()       #inside A4 method # follow MRO
        print("inside C4") 
comp1 = C4()

print("==========================")
#Polymorphism
#duck typing 
class Pycharm:
    def execute(self):
        print("running")
class MyEditor:
    def execute(self):
        print("good ruuning")
class Laptop:
    def code(self,ide):
        ide.execute()

ide=Pycharm()
lap=Laptop()
lap.code(ide)
ide=MyEditor()
lap=Laptop()
lap.code(ide)

# operator overloading
a=5
b=6
print(a+b)
print(int.__add__(a,b))  # behind the scene actually this is pappening

class Student11:
    def __init__(self,a,b):
        self.a=a
        self.b=b
    def __add__(self,other):
        d=self.a+other.a
        e=self.b+other.b
        c=Student11(d,e)
        return c
    def __str__(self):
        return '{} {}'.format(self.a,self.b)

s1=Student11(2,3)
s2=Student11(4,7)
s3=s1+s2 # measns s1._add(s2) but student calss dont know add hence override this, bcz only sum,minus know
print(s3.a)        

##__str__ method
print(a)  # print value 5 bcz interntally call a.__str__
print(s3) # print object internally call s3.__str__
# needs to ovverride __str__

#Method Overloading and Method Overriding
# python dont support method overloading but we do trick
class Car:
   
    def sum(self,a=None,b=None,c=None):
        if a!=None and b!=None and c!=None:
            return a+b+c
        if a!=None and b!=None:
            return a+b
        if a!=None:
            return a
     
        return a+b
c=Car()
print(c.sum(5, 7,6))
print(c.sum(5, 7))

# Mehod overriding
class A5:
    def f1(self):
        print("inside A")
        
class B5(A5):       
    def f2(self):
        print("inside B")
    
comp1 = B5()
comp1.f2() # if we call any method first we check its there in subclass or not, if not then check in super

#Exception Handling
#syntax Error=complile time error
#logical error= comiple but output is  wrong
#runtime error
a=4
b=0
try:
    print("resource open")
    d=a/b
    print("resource close") # only run when exceptio not come
    a=int('r')
except ZeroDivisionError as e:
    print("u cant dont devide by zero :",e)
except ValueError as e:
    print("Invaluid value :",e)
except Exception as e:
    print("Something wrong :",e)
finally:
    print("bye")
print("**************************")
# Multithreading
from time import sleep
class Hello(Thread):
    def run(self):
        for i in range(5):
            print("Hello")
            sleep(1)
            
class Hi(Thread):
    def run(self):
        for i in range(5):
            print("Hi")
            sleep(1)
            
h1=Hello()
h2=Hi()

h1.start()
sleep(0.2)
h2.start()

h1.join()
h2.join()
#file handling
#Read data
f = open('Read', 'r')
#print(f.read())
print("-------------")
print(f.readline(),end="")
print(f.readline())
print(f.readline(3)) # print only 3 char

#Write data
f1=open('abc','w')
f1.write("somthing")
f1.write("write")

#append data
f1=open('abc','a')
f1.write("somthing")
f1.write("write")
f1.write("write1")
print("::::::::::::::::::::::::::::")

#copy data from one file to another(read from one and write to another)
for data in f:
    f1.write(data)

#Read binary(img,pic/video) formt data
f1=open('img.jpg','rb') # usr rb to read binary filr pervious was char format
print(f1.read())

#copy binary data from one file to another(read from one and write to another)
f4=open('img1.jpg','wb')
for data in f1:
    f4.write(data)
    
#Comments in Python 
#python has only single line commets 
# documentation use """ triple cots

# python is compiled and interrator language both
# developer code - complier - byte code - interator(PVM-python virtual machine) 
# pythin different different implenatation flaour
# CPython- implemented in C python
# Jython -Implementation is in java
#IronPython - dot net version of python
# PyPy







        








