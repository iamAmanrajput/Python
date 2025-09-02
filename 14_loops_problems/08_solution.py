# Problem:
# Write a program to check whether a given number is prime or not.
# A prime number is a number greater than 1 that has no divisors
# other than 1 and itself.

number = 28
is_prime = True

if number > 1:
    for i in range(2, number):   # check divisibility
        if (number % i) == 0:    # if divisible, not prime
            is_prime = False
            break

print(is_prime)
