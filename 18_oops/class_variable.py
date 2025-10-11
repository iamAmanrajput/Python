# Problem: Add a class variable to Car that keeps track of the number of cars created.

class Car:
    # Class variable to track number of cars
    car_count = 0

    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        # Increment the class variable whenever a new Car is created
        Car.car_count += 1

    def display_info(self):
        print(f"Brand: {self.brand}, Model: {self.model}")

# Creating Car objects
car1 = Car("Toyota", "Corolla")
car2 = Car("Honda", "Civic")
car3 = Car("Ford", "Mustang")

# Display info
car1.display_info()
car2.display_info()
car3.display_info()

# Accessing the class variable
print("Total cars created:", Car.car_count)


# Brand: Toyota, Model: Corolla
# Brand: Honda, Model: Civic
# Brand: Ford, Model: Mustang
# Total cars created: 3
