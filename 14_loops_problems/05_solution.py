# Problem:
# Given a string, write a program to find the first non-repeated character.
# A non-repeated character is the one that appears only once in the string.

input_str = "teeteracdacd"

for char in input_str:
    print(char)  # just to show the iteration process
    if input_str.count(char) == 1:   # check if char appears only once
        print("Char is:", char)      # first unique char found
        break                        # stop after first match
