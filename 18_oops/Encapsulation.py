# Problem: Modify the Car class to encapsulate the brand attribute, making it private, and provide a getter method for it.

class Car:
    def __init__(self, brand, model):
        self.__brand = brand   # private attribute
        self.model = model

    # getter method for brand
    def get_brand(self):
        return self.__brand

# creating object of Car class
my_car = Car("BMW", "X5")

# accessing brand using getter method
print("Car Brand:", my_car.get_brand())
print("Car Model:", my_car.model)


# Car Brand: BMW
# Car Model: X5
