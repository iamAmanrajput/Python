# Basic Class and Object
# Create a Car class with attributes like brand and model. Then create an instance of this class.

class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

# creating an instance of the Car class
my_car = Car("Toyota", "Corolla")

# printing the attributes
print("Car Brand:", my_car.brand) # Car Brand: Toyota
print("Car Model:", my_car.model) # Car Model: Corolla
