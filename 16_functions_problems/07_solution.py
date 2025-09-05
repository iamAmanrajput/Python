# Problem:
# Write a Python function 'sum_all' that accepts any number of arguments 
# using *args. Inside the function:
# 1. Print the tuple of arguments.
# 2. Print each argument multiplied by 2.
# 3. Return the sum of all arguments.

def sum_all(*args):
    print(args)             # prints all arguments as a tuple
    for i in args:
        print(i * 2)        # print double of each argument
    return sum(args)        # return sum of arguments

print(sum_all(1, 2, 3))
# print(sum_all(1, 2, 3, 4, 5))
# print(sum_all(1, 2, 3, 4, 5, 6, 7, 8))

# Expected Output:
# (1, 2, 3)
# 2
# 4
# 6
# 6
