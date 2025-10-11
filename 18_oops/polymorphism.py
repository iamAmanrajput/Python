# Problem: Demonstrate polymorphism by defining a method fuel_type in both Car and ElectricCar classes, but with different behaviors.

class Car:
    def fuel_type(self):
        return "Petrol or Diesel"

class ElectricCar(Car):
    def fuel_type(self):
        return "Electric Battery"

# creating objects
car1 = Car()
car2 = ElectricCar()

# demonstrating polymorphism
print("Car Fuel Type:", car1.fuel_type())
print("Electric Car Fuel Type:", car2.fuel_type())


# Car Fuel Type: Petrol or Diesel
# Electric Car Fuel Type: Electric Battery
