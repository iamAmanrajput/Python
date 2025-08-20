# -------------------------------
# PYTHON DICTIONARY NOTES
# -------------------------------

# Dictionary ek data structure hai jo "key-value pairs" store karta hai.
# Syntax: dict = {key: value, key: value}

# Creating a dictionary
my_dict = {
    "name": "Aman",
    "age": 21,
    "city": "Delhi"
}
print(my_dict)
# Output: {'name': 'Aman', 'age': 21, 'city': 'Delhi'}

# Accessing values (using key)
print(my_dict["name"])   # Output: Aman

# Agar key exist nahi karti aur [] use kiya to error ayega
# print(my_dict["gender"])  # KeyError

# Safe access -> get() method (agar key na ho to None ya default return karega)
print(my_dict.get("gender"))        # Output: None
print(my_dict.get("gender", "N/A")) # Output: N/A

# Adding a new key-value pair
my_dict["country"] = "India"
print(my_dict)
# Output: {'name': 'Aman', 'age': 21, 'city': 'Delhi', 'country': 'India'}

# Updating value
my_dict["age"] = 22
print(my_dict["age"])  # Output: 22

# Removing elements
my_dict.pop("city")   # Removes key 'city'
print(my_dict)        
# Output: {'name': 'Aman', 'age': 22, 'country': 'India'}

# del keyword
del my_dict["country"]
print(my_dict)
# Output: {'name': 'Aman', 'age': 22}

# Looping in dictionary
for key in my_dict:
    print(key, ":", my_dict[key])
# Output:
# name : Aman
# age : 22

# Looping with items() (best way)
for k, v in my_dict.items():
    print(f"{k} -> {v}")
# Output:
# name -> Aman
# age -> 22

# Only keys
print(list(my_dict.keys()))  # ['name', 'age']

# Only values
print(list(my_dict.values()))  # ['Aman', 22]

# Dictionary length
print(len(my_dict))  # Output: 2

# Nesting (Dictionary inside Dictionary)
student = {
    "id": 101,
    "details": {
        "name": "Aman",
        "branch": "CSE",
        "skills": ["Python", "JavaScript"]
    }
}
print(student["details"]["skills"][0])  # Output: Python

# Dictionary Comprehension
squares = {x: x**2 for x in range(5)}
print(squares)
# Output: {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Important Methods
my_dict = {"a": 1, "b": 2, "c": 3}

print(my_dict.items())   # dict_items([('a', 1), ('b', 2), ('c', 3)])
print(my_dict.keys())    # dict_keys(['a', 'b', 'c'])
print(my_dict.values())  # dict_values([1, 2, 3])

# copy()
new_dict = my_dict.copy()
print(new_dict)  # {'a': 1, 'b': 2, 'c': 3}

# clear()
my_dict.clear()
print(my_dict)  # {}

# fromkeys() -> new dictionary with default values
keys = ["name", "age", "city"]
new_dict = dict.fromkeys(keys, "Unknown")
print(new_dict)
# Output: {'name': 'Unknown', 'age': 'Unknown', 'city': 'Unknown'}
