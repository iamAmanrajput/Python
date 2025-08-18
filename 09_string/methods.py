# Python String Important Methods with Examples

# 1. upper() - Converts all characters to uppercase
text = "hello world"
print(text.upper())  # Output: HELLO WORLD

# 2. lower() - Converts all characters to lowercase
text = "HELLO WORLD"
print(text.lower())  # Output: hello world

# 3. title() - Converts first character of each word to uppercase
text = "hello world"
print(text.title())  # Output: Hello World

# 4. capitalize() - Capitalizes first letter of the string
text = "hello world"
print(text.capitalize())  # Output: Hello world

# 5. strip() - Removes leading and trailing spaces
text = "   hello world   "
print(text.strip())  # Output: 'hello world'

# 6. lstrip() - Removes leading spaces
print(text.lstrip())  # Output: 'hello world   '

# 7. rstrip() - Removes trailing spaces
print(text.rstrip())  # Output: '   hello world'

# 8. replace(old, new) - Replaces substring with another
text = "I like Python"
print(text.replace("Python", "Java"))  # Output: I like Java

# 9. split() - Splits string into list
text = "apple,banana,cherry"
print(text.split(","))  # Output: ['apple', 'banana', 'cherry']

# 10. join() - Joins elements of list into string
fruits = ['apple', 'banana', 'cherry']
print(" - ".join(fruits))  # Output: apple - banana - cherry

# 11. find() - Returns index of first occurrence (-1 if not found)
text = "hello world"
print(text.find("world"))  # Output: 6

# 12. index() - Like find(), but raises error if not found
print(text.index("world"))  # Output: 6

# 13. count() - Counts occurrences of substring
print(text.count("l"))  # Output: 3

# 14. startswith() - Checks if string starts with substring
print(text.startswith("hello"))  # Output: True

# 15. endswith() - Checks if string ends with substring
print(text.endswith("world"))  # Output: True

# 16. isalpha() - Checks if all chars are alphabets
print("Python".isalpha())  # Output: True

# 17. isdigit() - Checks if all chars are digits
print("12345".isdigit())  # Output: True

# 18. isalnum() - Checks if all chars are alphanumeric
print("Python123".isalnum())  # Output: True

# 19. isspace() - Checks if all chars are whitespace
print("   ".isspace())  # Output: True

# 20. swapcase() - Swaps uppercase to lowercase and vice versa
print("Hello World".swapcase())  # Output: hELLO wORLD

# 21. zfill(width) - Pads string with leading zeros
print("42".zfill(5))  # Output: 00042

# 22. center(width, char) - Centers string with padding
print("hi".center(10, "*"))  # Output: ****hi****

# 23. ljust(width, char) - Left aligns string with padding
print("hi".ljust(10, "-"))  # Output: hi--------

# 24. rjust(width, char) - Right aligns string with padding
print("hi".rjust(10, "-"))  # Output: --------hi

# 25. format() - String formatting
name = "Aman"
age = 22
print("My name is {} and I am {} years old".format(name, age))
# Output: My name is Aman and I am 22 years old

# 26. f-string (Python 3.6+)
print(f"My name is {name} and I am {age} years old")
# Output: My name is Aman and I am 22 years old
