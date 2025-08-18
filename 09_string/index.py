# -----------------------------
# Python Strings Basics
# -----------------------------

# 1. String Creation
s1 = 'hello'
s2 = "world"
s3 = '''multi
line
string'''
print(s1, s2, s3)
# Output: hello world multi\nline\nstring

# 2. Indexing & Slicing
text = "Python"
print(text[0])    # P (first character)
print(text[-1])   # n (last character)
print(text[0:4])  # Pyth (0 se 3 tak)
print(text[2:])   # thon (index 2 se end tak)
print(text[:3])   # Pyt (start se index 2 tak)

# 3. Strings are Immutable
text = "hello"
# text[0] = 'H'  # ❌ Error (strings can't be changed)
text = "H" + text[1:]  # ✅ create new string
print(text)  # Hello

# 4. Concatenation & Repetition
a = "Hi"
b = "Aman"
print(a + " " + b)  # Hi Aman
print(a * 3)        # HiHiHi

# 5. Membership Test
sentence = "Python Programming"
print("Python" in sentence)   # True
print("Java" not in sentence) # True

# 6. Iterating over a String
for ch in "Aman":
    print(ch)
# Output:
# A
# m
# a
# n

# 7. Length of a String
print(len("hello"))  # 5
