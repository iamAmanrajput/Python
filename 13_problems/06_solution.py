# Problem Statement:
# Write a Python program that recommends a mode of transport based on the distance.
# - If the distance is less than 3 km, recommend "Walk".
# - If the distance is between 3 km and 15 km (inclusive), recommend "Bike".
# - If the distance is more than 15 km, recommend "Car".
# Finally, print the recommended mode of transport.

distance = 5

if distance < 3:
    transport = "Walk"
elif distance <= 15:
    transport = "Bike"
else:
    transport = "Car"

print("AI recommends you the transport of: ", transport)
