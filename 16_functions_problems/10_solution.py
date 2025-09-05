# Problem: Write a recursive function to calculate the factorial of a number.
# The factorial of n (written as n!) is defined as:
# n! = n * (n-1) * (n-2) * ... * 1
# Base Case: 0! = 1

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
