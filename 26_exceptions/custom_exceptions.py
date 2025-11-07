def brew_chai(flavor):
    if flavor not in ["masala", "ginger", "elaichai"]:
        raise ValueError("Unsupported chai flavor...")
    print(f"brewing {flavor} chai...")


brew_chai("mint")

# output

#  python -u "c:\AMAN\Python\26_exceptions\custom_exceptions.py"
# Traceback (most recent call last):
#   File "c:\AMAN\Python\26_exceptions\custom_exceptions.py", line 7, in <module>
#     brew_chai("mint")
#     ~~~~~~~~~^^^^^^^^
#   File "c:\AMAN\Python\26_exceptions\custom_exceptions.py", line 3, in brew_chai
#     raise ValueError("Unsupported chai flavor...")
# ValueError: Unsupported chai flavor... 