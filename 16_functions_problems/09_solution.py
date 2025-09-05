# Problem: Write a generator function that yields all even numbers 
# from 2 up to a given limit, and then iterate over the generator 
# to print each even number.

def even_generator(limit):
    for i in range(2, limit + 1, 2):
        yield i

for num in even_generator(10):
    print(num)
