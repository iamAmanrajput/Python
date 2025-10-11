# Problem: Demonstrate the use of isinstance() to check if my_tesla is an instance of Car and ElectricCar.

# Base class
class Car:
    def __init__(self, brand):
        self.brand = brand

# Derived class
class ElectricCar(Car):
    def __init__(self, brand, battery_capacity):
        super().__init__(brand)
        self.battery_capacity = battery_capacity

# Object create karte hain
my_tesla = ElectricCar("Tesla", 100)

# Check if my_tesla is instance of Car
print(isinstance(my_tesla, Car))        # Output: True

# Check if my_tesla is instance of ElectricCar
print(isinstance(my_tesla, ElectricCar)) # Output: True
