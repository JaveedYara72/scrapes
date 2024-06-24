# attributes are the variables that belong to a class
# attributes are always public and can be accessed using the dot


class Dog:
    pass

#object -> state, behavior, identity

obj = Dog() # creates an object named obj of the class Dog

# Self 
# by using self we can access the attributes and methods of the class in python.
# It binds the attributes with the given arguments
# Self is always pointing to Current Object.
class check:
    def __init__(self):
        print("Address of the self = ", id(self))

obj = check()
print("Address of the object = ", id(obj))


class car():
    def __init__(self,model,color):
        self.model = model
        self.color = color
    
    def show(self):
        print(self.model)
        print(self.color)


audi = car("Audi R8", "Red")
Mercedes = car("Mercedes Maybach", "Black")

audi.show()
Mercedes.show()

print("The Color of Audi is ", audi.color)
print("The Model of the Mercedes is ", Mercedes.model)

# __init__ method is like a constructor
class Dog:
    species = "Mammal"

    def __init__(self,name):
        self.name = name

    def speak(self):
        print("My Name is {}".format(self.name))


Rodger = Dog("Rodger")
Tommy = Dog("Tommy")


Rodger.speak()
Tommy.speak()


# Inheritance
# one class deriving or inheriting the properties from another class. 
#  parent class


class Person(object):
    def __init__(self,name, idnumber):
        self.name = name
        self.idnumber = idnumber
    
    def display(self):
        print(self.name)
        print(self.idnumber)

    def details(self):
        print("My name is {}".format(self.name))
        print("My idnumber is {}".format(self.idnumber))

class Employee(Person):
    def __init__(self,name,idnumber,salary,post):
        self.salary = salary
        self.post = post

        # Invoke the __init__ of the parent
        # this is when it would inherit the parent class
        Person.__init__(self,name,idnumber)
    
    def details(self):
        print("My name is {}".format(self.name))
        print("My idnumber is {}".format(self.idnumber))
        print("My Salary is {}".format(self.salary))
        print("My Role is {}".format(self.post))


a = Employee('Sampath',1901220, 600000000, 'SDE')

a.details()

# Polymorphism
# it simply means having multiple forms

class Cricketer:
    def __init__(self):
        print("There are many types of birds")
    
    def type_of(self):
        print("A Cricketer can either be a Bowler, Batsman, Fielder, Wicketkeeper")


class kl_rahul(Cricketer):
    def type_of(self):
        print("I am a Wicket keeper/ batsman")

class Zaheer_Khan(Cricketer):
    def type_of(self):
        print("I am a bowler, and i love eating vadapav")

class VK(Cricketer):
    def type_of(self):
        print("I am a batsman")


obj_Crick = Cricketer()
obj_sarfaraz = kl_rahul()
obj_siraj = Zaheer_Khan()
obj_Shubman = VK()


obj_Crick.type_of()
obj_sarfaraz.type_of()
obj_siraj.type_of()
obj_Shubman.type_of()

# to hide anything in a class which cant be accessed from outside
# put a double underscore before that variable


# Encapsulation
# class Base:
#     def __init__(self):
#         self.a = "Virgil Van Dijk"
#         self.__c = "Jurgen Klopp"

# class Derived(Base):
#     def __init__(self):
#         Base.__init__(self) # why cant i access the __c from the base clas
#         print("Calling the private member of the class")
#         print(self.__c)
# obj = Base()
# obj1 = Derived(obj)
# print(obj1.a)

class MyClass:
    def __init__(self):
        __hiddenvariable = 72
        self.hiddenvariable = 72

    def add(self,increment):
        self.hiddenvariable+=increment
        # print(hiddenvariable)
        # self.__hiddenvariable += increment
        print(self.hiddenvariable)

encapobj = MyClass()
a=encapobj.add(2)
print(type(a))
encapobj = MyClass()
encapobj.add(5)

# will this hidden variable be note resetting to 72 everytime i call it?
# why is that?


class Vehicle:
    def __init__(self,max_speed,mileage):
        self.max_speed = max_speed
        self.mileage =  mileage

    def show(self):
        print(self.max_speed)
        print(self.mileage)

class Vehicle_2:
    pass


class Vehicle_3(object):

    def __init__(self, name, max_speed, mileage,color = "white"):
        self.name = name
        self.max_speed = max_speed
        self.mileage = mileage
        self.color = color
    
    def seating_capacity(self,capacity):
        print(f"The seating capacity of a {self.name} is {capacity} passengers")

class Bus(Vehicle_3):
    def __init__(self,name,max_speed,mileage,color):
        Vehicle_3.__init__(self,name,max_speed,mileage,color="white")
        print(self.name)
        print(self.max_speed)
        print(self.mileage)
        print(self.color)
    
    def seating_capacity(self, capacity):
        return super().seating_capacity(capacity=50)

    

class Car(Vehicle_3):
    def __init__(self,name,max_speed,mileage,color):
        Vehicle_3.__init__(self,name,max_speed,mileage,color="white")
        print(self.color)


class Vehicle_4:
    def __init__(self,name,max_speed,mileage,capacity):
        self.name = name
        self.mileage= mileage
        self.capacity = capacity
        self.max_speed = max_speed

    def fare(self):
        print(f"The fare for this bus would be {(self.capacity)*50}")

class Bus_1(Vehicle_4):
    def __init__(self,name, max_speed, mileage,capacity):
        Vehicle_4.__init__(self,name, max_speed, mileage, capacity)


if __name__ == "__main__":
    # the main function of python 
    tata_nano = Vehicle(60,20)
    tata_nano.show()

    rtc = Bus("rtc",40,9,"Random")
    rtc.seating_capacity(40)

    ferrari = Car("Ferrari 416",300,4,"Random")

    school_bus = Bus_1("school",30,5,100)
    school_bus.fare()
