# 1. String (immutable)
name = "hello"
# name[0] = "H"  # Error: cannot directly change characters in a string
name = "Hello"  # created a new string
print(name)  # Hello

# 2. Tuple (immutable)
colors = ("red", "green", "blue")
# colors[0] = "yellow"  # Error: cannot change elements of a tuple

# 3. Integer (immutable)
x = 10
# x[0] = 5  # Error: integers have no items to change
x = 20  # created a new integer
print(x)  # 20
