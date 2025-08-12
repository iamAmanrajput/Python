# 1. List (mutable)
fruits = ["apple", "banana", "mango"]
fruits[1] = "grapes"  # changed 'banana' to 'grapes'
print(fruits)  # ['apple', 'grapes', 'mango']

# 2. Dictionary (mutable)
person = {"name": "Aman", "age": 21}
person["age"] = 22  # updated the value of 'age'
print(person)  # {'name': 'Aman', 'age': 22}

# 3. Set (mutable)
numbers = {1, 2, 3}
numbers.add(4)  # added a new element to the set
print(numbers)  # {1, 2, 3, 4}
