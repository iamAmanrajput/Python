# ==============================================
# Python Internal Working Examples
# Copy | Reference Counts | Slice
# ==============================================

import sys
import copy

print("\n================= 1. COPY =================")

# 1.1 Assignment (No copy, only reference)
print("\n-- Assignment (No copy, only reference) --")
a = [1, 2, 3]
b = a  # same reference
b[0] = 99
print("a:", a)  # [99, 2, 3]
print("a is b:", a is b)  # True

# OUTPUT:
# a: [99, 2, 3]
# a is b: True


# 1.2 Shallow Copy
print("\n-- Shallow Copy --")
a = [[1, 2], [3, 4]]
b = copy.copy(a)
b[0][0] = 99
print("a:", a)  # inner list change ho gayi
print("a is b:", a is b)       # False
print("a[0] is b[0]:", a[0] is b[0]) # True

# OUTPUT:
# a: [[99, 2], [3, 4]]
# a is b: False
# a[0] is b[0]: True


# 1.3 Deep Copy
print("\n-- Deep Copy --")
a = [[1, 2], [3, 4]]
b = copy.deepcopy(a)
b[0][0] = 99
print("a:", a)  # no change
print("a is b:", a is b)       # False
print("a[0] is b[0]:", a[0] is b[0]) # False

# OUTPUT:
# a: [[1, 2], [3, 4]]
# a is b: False
# a[0] is b[0]: False


print("\n================= 2. REFERENCE COUNTS =================")

a = [1, 2, 3]
print("\nInitial ref count of a:", sys.getrefcount(a))  # extra +1 due to function call

b = a
print("After assigning b = a, ref count:", sys.getrefcount(a))

del b
print("After deleting b, ref count:", sys.getrefcount(a))

# OUTPUT (numbers thode system ke hisaab se vary karenge):
# Initial ref count of a: 2
# After assigning b = a, ref count: 3
# After deleting b, ref count: 2


print("\n================= 3. SLICE =================")

# 3.1 Slice on list
print("\n-- Slice on list --")
a = [1, 2, 3, 4, 5]
b = a[1:4]
print("Slice result:", b)  # [2, 3, 4]
print("a is b:", a is b)  # False

# OUTPUT:
# Slice result: [2, 3, 4]
# a is b: False


# 3.2 Slice on string
print("\n-- Slice on string --")
s = "Python"
sub = s[0:3]
print("Substring:", sub)  # Pyt

# OUTPUT:
# Substring: Pyt


# 3.3 Slice = shallow copy
print("\n-- Slice shallow copy behaviour --")
a = [[1, 2], [3, 4]]
b = a[:]
b[0][0] = 99
print("a after modifying b:", a)  # inner list change ho gayi
print("a is b:", a is b)       # False
print("a[0] is b[0]:", a[0] is b[0]) # True

# OUTPUT:
# a after modifying b: [[99, 2], [3, 4]]
# a is b: False
# a[0] is b[0]: True


print("\n================= END =================")
