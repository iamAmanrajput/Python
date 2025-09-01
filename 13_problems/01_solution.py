# Problem Statement:
# Write a Python program that determines a person's life stage based on their age.
# - If the age is less than 13, print "Child".
# - If the age is between 13 and 19, print "Teenager".
# - If the age is between 20 and 59, print "Adult".
# - If the age is 60 or above, print "Senior".

age = 65

if age < 13:
    print("Child")
elif age < 20:
    print("Teenager")
elif age < 60:
    print("Adult")
else:
    print("Senior")
