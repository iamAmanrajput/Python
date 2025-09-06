def outer_function(msg):
    # 'msg' is a variable defined in outer_function

    def inner_function():
        # inner_function is using 'msg' from outer_function
        print("Message:", msg)

    return inner_function  # returning the inner function


# Calling outer_function
closure = outer_function("Hello Closure")

# outer_function has finished execution,
# but inner_function still remembers the value of 'msg'
closure()
