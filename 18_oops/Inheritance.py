# Problem : Create an ElectricCar class that inherits from the Car class and has an additional attribute battery_size.

# Parent class
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

# Child class
class ElectricCar(Car):
    def __init__(self, brand, model, battery_size):
        # inherit brand and model from Car class
        super().__init__(brand, model)
        self.battery_size = battery_size

# creating an instance of ElectricCar
my_electric_car = ElectricCar("Tesla", "Model S", "100 kWh")

# displaying information
print("Brand:", my_electric_car.brand)
print("Model:", my_electric_car.model)
print("Battery Size:", my_electric_car.battery_size)


# Brand: Tesla
# Model: Model S
# Battery Size: 100 kWh
