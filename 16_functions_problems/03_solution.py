# Problem:
# Write a Python function called 'multiply' that takes two parameters (p1 and p2)
# and returns their multiplication. Demonstrate the function with:
# 1. Two numbers
# 2. A string and a number
# 3. A number and a string

def multiply(p1, p2):
    return p1 * p2  # returns the product of p1 and p2

# Example calls:
print(multiply(8, 5))      # Case 1: Multiplying two numbers → 40
print(multiply('a', 5))    # Case 2: String * number → 'aaaaa'
print(multiply(5, 'a'))    # Case 3: Number * string → 'aaaaa'
