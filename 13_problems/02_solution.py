# Problem Statement:
# Write a Python program to calculate movie ticket price based on age and day of the week.
# - If the person is 18 years or older, the ticket price is $12.
# - If the person is younger than 18, the ticket price is $8.
# - On Wednesdays, everyone gets a $2 discount on the ticket price.
# Finally, print the ticket price.

age = 26
day = "Wednesday"

price = 12 if age >= 18 else 8

if day == "Wednesday":
    # Apply $2 discount on Wednesday
    price -= 2

print("Ticket price for you is $", price)
