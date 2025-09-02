# Problem:
# Write a program to reverse a given string without using built-in reverse functions.
# The program should take a string and build the reversed version character by character.

input_str = "Python"
reversed_str = ""

for char in input_str:
    reversed_str = char + reversed_str   # add char in front each time

print(reversed_str)
