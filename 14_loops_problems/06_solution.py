# Problem:
# Write a program to calculate the factorial of a given number using a while loop.
# Factorial of n (written as n!) is the product of all positive integers from n down to 1.
# Example: 5! = 5 × 4 × 3 × 2 × 1 = 120

number = 5
factorial = 1

while number > 0:
    factorial *= number   # multiply current number
    number -= 1           # decrease number by 1

print("Factorial:", factorial)
