# Problem: Add a method to the Car class that displays the full name of the car (brand and model).

class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    # method to display full name
    def display_full_name(self):
        print(f"Car Name: {self.brand} {self.model}")

# creating an instance of Car class
my_car = Car("Hyundai", "Creta")

# calling the method
my_car.display_full_name()

# Car Name: Hyundai Creta
