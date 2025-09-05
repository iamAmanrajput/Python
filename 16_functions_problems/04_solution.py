# Problem:
# Write a Python function 'circle_stats' that takes the radius of a circle
# and returns both its area and circumference using the math module.

import math

def circle_stats(radius):
    area = math.pi * radius ** 2        # π * r^2
    circumference = 2 * math.pi * radius  # 2 * π * r
    return area, circumference

a, c = circle_stats(3)

print("Area:", a, "Circumference:", c)

# Expected Output:
# Area: 28.274333882308138 Circumference: 18.84955592153876
