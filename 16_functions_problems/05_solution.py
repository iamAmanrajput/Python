# Problem:
# Write a Python function 'greet' that takes a name as input 
# and returns a greeting message. 
# If no name is provided, use "User" as the default value.

def greet(name = "User"):
    return "Hello, " + name + " !"   # function returns greeting

print(greet("chai"))   # passing argument
print(greet())         # using default parameter

# Expected Output:
# Hello, chai !
# Hello, User !
