# Problem:
# Given a number n, write a program to calculate the sum of all even numbers
# from 1 to n (inclusive) and print the result.

n = 10
sum_even = 0

for i in range(1, n+1):
    if i % 2 == 0:
        sum_even += i 

print("Sum of even numbers is:", sum_even)
