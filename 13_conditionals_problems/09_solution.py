# Problem Statement:
# Write a Python program to check whether a given year is a leap year or not.
# - A year is a leap year if it is divisible by 400.
# - Or, if it is divisible by 4 but not divisible by 100.
# - Otherwise, it is not a leap year.
# Print the result accordingly.

year = 2023

if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
    print(year, "is a leap year")
else:
    print(year, "is NOT a leap year")
