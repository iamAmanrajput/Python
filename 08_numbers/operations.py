# Basic Number Operations in Python

# Two sample numbers
a = 15
b = 4

# Addition (+) → Adds two numbers
addition = a + b
print("Addition:", addition)  # 15 + 4 = 19

# Subtraction (-) → Subtracts second number from first
subtraction = a - b
print("Subtraction:", subtraction)  # 15 - 4 = 11

# Multiplication (*) → Multiplies numbers
multiplication = a * b
print("Multiplication:", multiplication)  # 15 * 4 = 60

# Division (/) → Always returns float in Python
division = a / b
print("Division:", division)  # 15 / 4 = 3.75

# Floor Division (//) → Divides and rounds down to nearest integer
floor_division = a // b
print("Floor Division:", floor_division)  # 15 // 4 = 3

# Modulus (%) → Returns remainder of division
modulus = a % b
print("Modulus:", modulus)  # 15 % 4 = 3

# Exponentiation (**) → Raises number to power
exponentiation = a ** b
print("Exponentiation:", exponentiation)  # 15^4 = 50625

# ------------------------------
# Operator precedence (BODMAS rule)
result = a + b * 2   # Multiplication happens first
print("Operator precedence:", result)  # 15 + (4*2) = 23

# ------------------------------
# Mixing integers and floats
c = 7.5
d = 2
print("Float + Int:", c + d)   # 7.5 + 2 = 9.5
print("Float * Int:", c * d)   # 7.5 * 2 = 15.0

# ------------------------------
# Built-in functions for numbers
print("Absolute value:", abs(-10))  # |-10| = 10
print("Round off:", round(3.14159, 2))  # Round to 2 decimal places → 3.14
