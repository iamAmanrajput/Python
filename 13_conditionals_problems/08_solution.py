# Problem Statement:
# Write a Python program to check the strength of a password based on its length.
# - If the password length is less than 6 characters, it is considered "Weak".
# - If the password length is between 6 and 10 characters (inclusive), it is considered "Medium".
# - If the password length is more than 10 characters, it is considered "Strong".
# Finally, print the password strength.

password = "Secure3P@ss"
password_length = len(password)

if len(password) < 6:
    strength = "Weak"
elif len(password) <= 10:
    strength = "Medium"
else:
    strength = "Strong"

print("Password strength is: ", strength)
