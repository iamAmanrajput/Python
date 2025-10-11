# Problem: Add a static method to the Car class that returns a general description of a car.

class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    @staticmethod
    def general_description():
        return "A car is a vehicle with four wheels used for transporting people."

# Creating Car objects
car1 = Car("Toyota", "Corolla")
car2 = Car("Honda", "Civic")

# Calling the static method via class
print(Car.general_description())

# Calling the static method via instance
print(car1.general_description())


# A car is a vehicle with four wheels used for transporting people.
# A car is a vehicle with four wheels used for transporting people.
