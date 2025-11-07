class OutOfIngredientsError(Exception):
    pass

def make_chai(milk, sugar):
    if milk == 0 or sugar == 0:
        raise OutOfIngredientsError("Missing milk or sugar")
    print("chai is ready...")


make_chai(0, 1)

# output

# python -u "c:\AMAN\Python\26_exceptions\custom_error_class.py"
# Traceback (most recent call last):
#   File "c:\AMAN\Python\26_exceptions\custom_error_class.py", line 10, in <module>
#     make_chai(0, 1)
#     ~~~~~~~~~^^^^^^
#   File "c:\AMAN\Python\26_exceptions\custom_error_class.py", line 6, in make_chai
#     raise OutOfIngredientsError("Missing milk or sugar")
# OutOfIngredientsError: Missing milk or sugar