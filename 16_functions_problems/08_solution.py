# Problem:
# Write a Python function 'print_kwargs' that accepts any number of 
# keyword arguments using **kwargs and prints each key-value pair.

def print_kwargs(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# function calls with different keyword arguments
print_kwargs(name="shaktiman", power="lazer")
print_kwargs(name="shaktiman")
print_kwargs(name="shaktiman", power="lazer", enemy="Dr. Jackaal")

# Expected Output:
# name: shaktiman
# power: lazer
# name: shaktiman
# name: shaktiman
# power: lazer
# enemy: Dr. Jackaal
