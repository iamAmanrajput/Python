# Problem:
# Write a program that keeps asking the user to enter a number between 1 and 10.
# If the entered number is valid (1 to 10), print "Thanks" and stop the loop.
# Otherwise, keep asking until the user enters a valid number.

while True:
    number = int(input("Enter value b/w 1 and 10: "))
    if 1 <= number <= 10:    # check if number is in range
        print("Thanks")
        break                # exit loop if valid
    else:
        print("Invalid number, try again")
