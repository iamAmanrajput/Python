# Problem:
# Given a list of items, write a program to find the first duplicate item.
# The program should use a set to keep track of seen items.
# As soon as a duplicate is found, print it and stop the loop.

items = ["apple", "banana", "orange", "apple", "mango"]

unique_item = set()

for item in items:
    if item in unique_item:      # already seen -> duplicate found
        print("Duplicate:", item)
        break
    unique_item.add(item)        # add item to set if not duplicate
