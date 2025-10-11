# Problem: Use a property decorator in the Car class to make the model attribute read-only.

class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self._model = model  # _model ko private jaisa treat karenge

    # Getter method using property decorator
    @property
    def model(self):
        return self._model

# Creating a Car object
car1 = Car("Toyota", "Corolla")

# Accessing the model (works)
print(car1.model)  # Output: Corolla

# Trying to modify the model (will raise error)
car1.model = "Honda Civic"  # AttributeError: can't set attribute
