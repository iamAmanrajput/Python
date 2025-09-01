# Problem Statement:
# Write a Python program to check the ripeness of a banana based on its color.
# - If the fruit is "Banana":
#     - If the color is "Green", print "Unripe".
#     - If the color is "Yellow", print "Ripe".
#     - If the color is "Brown", print "OverRipe".

fruit = "Banana"
color = "Yellow"

if fruit == "Banana":
    if color == "Green":
        print("Unripe")
    elif color == "Yellow":
        print("Ripe")
    elif color == "Brown":
        print("OverRipe")
