# =========================
# PYTHON LIST BASICS & MANIPULATION
# =========================

# 1️ List creation
list1 = [1, 2, 3, 4, 5]           # integer list
list2 = ["apple", "banana", "cherry"]  # string list
list3 = [1, "hello", 3.14, True]  # mixed list
list4 = []                         # empty list

# 2️ Accessing elements
print(list1[0])   # first element: 1
print(list1[-1])  # last element: 5

# 3️ Slicing
print(list1[1:4])   # index 1 to 3: [2,3,4]
print(list1[:3])    # first 3 elements: [1,2,3]
print(list1[2:])    # from index 2 to end: [3,4,5]
print(list1[:])     # full copy: [1,2,3,4,5]

# 4️ Modifying elements
list1[0] = 10      # change first element
print(list1)       # [10,2,3,4,5]

# 5️ Adding elements
list1.append(6)          # add at end
list1.insert(2, 99)      # insert 99 at index 2
list1.extend([7, 8, 9])  # add multiple elements
print(list1)             # [10,2,99,3,4,5,6,7,8,9]

# 6️ Removing elements
list1.pop()           # remove last element
list1.pop(2)          # remove element at index 2
list1.remove(4)       # remove first occurrence of value 4
print(list1)          # [10,2,3,5,6,7,8]

# 7️ Searching / Checking elements
print(3 in list1)        # True
print(list1.index(5))    # index of value 5

# 8 Length of list
print(len(list1))        # number of elements

# 9️ Sorting & reversing
numbers = [5, 2, 9, 1, 5, 6]
numbers.sort()           # ascending
print(numbers)           # [1,2,5,5,6,9]
numbers.sort(reverse=True)  # descending
print(numbers)           # [9,6,5,5,2,1]

numbers.reverse()        # reverse current list
print(numbers)           # [1,2,5,5,6,9]

# 10 Copying lists
list_a = [1,2,3]
list_b = list_a           # reference copy
list_c = list_a[:]        # independent copy
list_c.append(4)
print(list_a)             # [1,2,3]
print(list_c)             # [1,2,3,4]

# 1️1️ Nested lists (lists inside list)
nested = [[1,2], [3,4], [5,6]]
print(nested[0])      # [1,2]
print(nested[1][1])   # 4

# 1️2️ Iterating through list
for item in list2:
    print(item)

# 1️3️ List comprehension (quick way to make new list)
squares = [x**2 for x in range(1,6)]  # [1,4,9,16,25]
even_nums = [x for x in range(10) if x%2==0]  # [0,2,4,6,8]

# 1️4️ Clearing a list
list4 = [1,2,3]
list4.clear()  # becomes empty
print(list4)   # []

#  Summary:
# Lists are mutable, ordered collections in Python.
# You can add, remove, modify, slice, search, sort, iterate, and copy them.

