# Problem: Create two classes Battery and Engine, and let the ElectricCar class inherit from both, demonstrating multiple inheritance.


# First parent class
class Battery:
    def __init__(self, battery_capacity):
        self.battery_capacity = battery_capacity

    def show_battery(self):
        print(f"Battery capacity: {self.battery_capacity} kWh")

# Second parent class
class Engine:
    def __init__(self, engine_type):
        self.engine_type = engine_type

    def show_engine(self):
        print(f"Engine type: {self.engine_type}")

# Child class inheriting from both Battery and Engine
class ElectricCar(Battery, Engine):
    def __init__(self, brand, battery_capacity, engine_type):
        self.brand = brand
        Battery.__init__(self, battery_capacity)
        Engine.__init__(self, engine_type)

    def show_info(self):
        print(f"Brand: {self.brand}")
        self.show_battery()
        self.show_engine()

# Creating an object of ElectricCar
my_tesla = ElectricCar("Tesla", 100, "Electric Motor")

# Displaying information
my_tesla.show_info()


# Brand: Tesla
# Battery capacity: 100 kWh
# Engine type: Electric Motor
