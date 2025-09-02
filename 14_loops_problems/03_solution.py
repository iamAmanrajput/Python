# Problem:
# Write a program to print the multiplication table of a given number.
# However, skip the multiplication when the multiplier is 5 (using 'continue').

number = 3

for i in range(1, 11):
    if i == 5:       # when i = 5, skip this iteration
        continue
    print(number, 'x', i, '=', number * i)
