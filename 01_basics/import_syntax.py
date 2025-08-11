# Import the print_this function from the hello.py file (in the same folder or Python path)
from hello import print_this

# Call the imported function with 20
print_this(20)

# Expected Output:
# hello bro   # This comes from hello.py because it has a print("hello bro") at the top
# 10          # This also comes from hello.py because when hello.py was run during import,
#             # it called print_this(10)
# 20          # This comes from the function call here
