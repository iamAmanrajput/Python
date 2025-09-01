# Problem Statement:
# Write a Python program to generate a coffee order description.
# - The order has a size: "Small", "Medium", or "Large".
# - If the customer wants an extra shot, add "with an extra shot" to the order.
# - Otherwise, just mention the coffee size.
# Finally, print the complete order.

order_size = "Medium"
extra_shot = True

if extra_shot:
    coffee = order_size + " coffee with an extra shot"
else:
    coffee = order_size + " coffee"

print("Order: ", coffee)
