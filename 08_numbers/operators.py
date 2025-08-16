# Python Operators - Full Example with Comments and Outputs

# -----------------------------
# 1. Arithmetic Operators
# -----------------------------
a = 10
b = 3
print("Arithmetic Operators:")
print("Addition:", a + b)         # 10 + 3 = 13
print("Subtraction:", a - b)      # 10 - 3 = 7
print("Multiplication:", a * b)   # 10 * 3 = 30
print("Division:", a / b)         # 10 / 3 = 3.333...
print("Floor Division:", a // b)  # 10 // 3 = 3
print("Modulus:", a % b)          # 10 % 3 = 1 (remainder)
print("Exponentiation:", a ** b)  # 10^3 = 1000
print("-" * 40)

# -----------------------------
# 2. Comparison Operators
# -----------------------------
print("Comparison Operators:")
print("a == b:", a == b)   # False
print("a != b:", a != b)   # True
print("a > b:", a > b)     # True
print("a < b:", a < b)     # False
print("a >= b:", a >= b)   # True
print("a <= b:", a <= b)   # False
print("-" * 40)

# -----------------------------
# 3. Logical Operators
# -----------------------------
x = True
y = False
print("Logical Operators:")
print("x and y:", x and y)   # False (both must be True)
print("x or y:", x or y)     # True (at least one True)
print("not x:", not x)       # False (reverse value)
print("-" * 40)

# -----------------------------
# 4. Bitwise Operators
# -----------------------------
# a = 10 (binary: 1010), b = 3 (binary: 0011)
print("Bitwise Operators:")
print("a & b:", a & b)   # AND  -> 1010 & 0011 = 0010 (2)
print("a | b:", a | b)   # OR   -> 1010 | 0011 = 1011 (11)
print("a ^ b:", a ^ b)   # XOR  -> 1010 ^ 0011 = 1001 (9)
print("~a:", ~a)         # NOT  -> -(a+1) = -11
print("a << 1:", a << 1) # Left shift  -> 1010 << 1 = 10100 (20)
print("a >> 1:", a >> 1) # Right shift -> 1010 >> 1 = 0101 (5)
print("-" * 40)

# -----------------------------
# 5. Assignment Operators
# -----------------------------
c = 5
print("Assignment Operators:")
c += 3  # c = c + 3
print("c after += 3:", c)
c -= 2  # c = c - 2
print("c after -= 2:", c)
c *= 4  # c = c * 4
print("c after *= 4:", c)
c /= 3  # c = c / 3
print("c after /= 3:", c)
c //= 2 # c = c // 2
print("c after //= 2:", c)
c %= 2  # c = c % 2
print("c after %= 2:", c)
c = 2
c **= 3 # c = c ** 3
print("c after **= 3:", c)
c &= 1  # bitwise AND assignment
print("c after &= 1:", c)
print("-" * 40)

# -----------------------------
# 6. Membership Operators
# -----------------------------
nums = [1, 2, 3, 4]
print("Membership Operators:")
print("2 in nums:", 2 in nums)       # True
print("5 in nums:", 5 in nums)       # False
print("5 not in nums:", 5 not in nums) # True
print("-" * 40)

# -----------------------------
# 7. Identity Operators
# -----------------------------
p = [1, 2]
q = p
r = [1, 2]
print("Identity Operators:")
print("p is q:", p is q)       # True (same object in memory)
print("p is r:", p is r)       # False (different objects)
print("p is not r:", p is not r) # True
