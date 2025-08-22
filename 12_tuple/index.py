# -------------------------------
# 1. Tuple Definition
# -------------------------------
# Tuple ek ordered, immutable (badla nahi ja sakta) collection hai.
# Ye list ki tarah hota hai, but isme changes (add/remove/update) nahi kar sakte.

# Empty tuple
t1 = ()
print(t1)   # Output: ()

# Single element tuple (comma lagana zaroori hai)
t2 = (5,)
print(t2)   # Output: (5,)

# Multiple elements
t3 = (1, 2, 3, 4)
print(t3)   # Output: (1, 2, 3, 4)

# Mixed data types
t4 = (10, "hello", 3.5, True)
print(t4)   # Output: (10, 'hello', 3.5, True)


# -------------------------------
# 2. Accessing Tuple Elements
# -------------------------------
# Indexing (0-based hoti hai, bilkul list ki tarah)
t = (100, 200, 300, 400)

print(t[0])   # Output: 100
print(t[2])   # Output: 300

# Negative Indexing (right side se count hota hai)
print(t[-1])  # Output: 400
print(t[-2])  # Output: 300


# -------------------------------
# 3. Tuple Slicing
# -------------------------------
t = (1, 2, 3, 4, 5, 6)

print(t[1:4])   # Output: (2, 3, 4)   -> index 1 se lekar 3 tak
print(t[:3])    # Output: (1, 2, 3)   -> 0 se 2 tak
print(t[3:])    # Output: (4, 5, 6)   -> 3 se end tak
print(t[-3:])   # Output: (4, 5, 6)   -> last 3 elements


# -------------------------------
# 4. Tuple Operations
# -------------------------------

# Concatenation (Do tuples ko jodna)
t1 = (1, 2)
t2 = (3, 4)
print(t1 + t2)   # Output: (1, 2, 3, 4)

# Repetition
t3 = ("Hi",) * 3
print(t3)        # Output: ('Hi', 'Hi', 'Hi')

# Membership Test
print(2 in (1, 2, 3))   # Output: True
print(5 not in (1, 2, 3))  # Output: True


# -------------------------------
# 5. Tuple Functions
# -------------------------------
t = (10, 20, 30, 40, 10)

print(len(t))      # Output: 5  -> total elements
print(max(t))      # Output: 40 -> max value
print(min(t))      # Output: 10 -> min value
print(t.count(10)) # Output: 2  -> 10 kitni baar aaya
print(t.index(30)) # Output: 2  -> 30 ka index


# -------------------------------
# 6. Tuple Packing and Unpacking
# -------------------------------
# Packing (multiple values ko tuple me dalna)
t = 1, "Hello", 3.14
print(t)   # Output: (1, 'Hello', 3.14)

# Unpacking (tuple ke values ko alag variables me lena)
a, b, c = t
print(a)   # Output: 1
print(b)   # Output: Hello
print(c)   # Output: 3.14


# -------------------------------
# 7. Nested Tuples
# -------------------------------
t = (1, (2, 3), (4, 5, 6))
print(t[1])      # Output: (2, 3)
print(t[2][1])   # Output: 5


# -------------------------------
# 8. Why use Tuple?
# -------------------------------
# - Fast hote hain list se (performance me)
# - Immutable hone ki wajah se data safe rehta hai
# - Dictionaries me key ke roop me use kar sakte ho (list nahi ho sakti)
