# 1. Numeric Types

# Integer (whole numbers)
a = 10           # int
print(a, type(a))  # 10 <class 'int'>

# Float (decimal numbers)
b = 3.14         # float
print(b, type(b))  # 3.14 <class 'float'>

# Complex numbers (real + imaginary part)
c = 2 + 3j       # complex
print(c, type(c))  # (2+3j) <class 'complex'>


# 2. Sequence Types

# String (immutable sequence of characters)
name = "Python"
print(name, type(name))  # Python <class 'str'>

# List (mutable sequence)
fruits = ["apple", "banana", "cherry"]
print(fruits, type(fruits))  # ['apple', 'banana', 'cherry'] <class 'list'>

# Tuple (immutable sequence)
colors = ("red", "green", "blue")
print(colors, type(colors))  # ('red', 'green', 'blue') <class 'tuple'>

# Range (sequence of numbers)
r = range(5)  # 0, 1, 2, 3, 4
print(list(r), type(r))  # [0, 1, 2, 3, 4] <class 'range'>


# 3. Mapping Type

# Dictionary (key-value pairs, mutable)
person = {"name": "Aman", "age": 21}
print(person, type(person))  # {'name': 'Aman', 'age': 21} <class 'dict'>



# 4. Set Types

# Set (unordered, unique values)
numbers = {1, 2, 3, 3}  # duplicates removed automatically
print(numbers, type(numbers))  # {1, 2, 3} <class 'set'>

# Frozenset (immutable set)
f_numbers = frozenset({1, 2, 3})
print(f_numbers, type(f_numbers))  # frozenset({1, 2, 3}) <class 'frozenset'>



# 5. Boolean Type

# Boolean (True or False)
is_active = True
print(is_active, type(is_active))  # True <class 'bool'>



# 6. None Type

# None (represents absence of value)
x = None
print(x, type(x))  # None <class 'NoneType'>



# 7. Binary Types

# Bytes (immutable sequence of bytes)
data = b"hello"
print(data, type(data))  # b'hello' <class 'bytes'>

# Bytearray (mutable sequence of bytes)
data_arr = bytearray(b"hello")
print(data_arr, type(data_arr))  # bytearray(b'hello') <class 'bytearray'>

# Memoryview (memory view object)
mv = memoryview(b"hello")
print(mv, type(mv))  # <memory at 0x...> <class 'memoryview'>
  


