# ===============================
# Python Scope (LEGB Rule)
# L → Local, E → Enclosed, G → Global, B → Built-in
# ===============================

# ----- Global Scope -----
x = "I am Global"

def outer_function():
    # ----- Enclosed Scope -----
    x = "I am Enclosed"

    def inner_function():
        # ----- Local Scope -----
        x = "I am Local"
        print("Local:", x)  # Local scope variable used

    inner_function()
    print("Enclosed:", x)  # Enclosed scope variable used


outer_function()
print("Global:", x)  # Global scope variable used


# ----- Built-in Scope -----
# Example: len() is a built-in function in Python
my_list = [1, 2, 3, 4]
print("Built-in (len):", len(my_list))  # Built-in scope


"""
OUTPUT:
Local: I am Local
Enclosed: I am Enclosed
Global: I am Global
Built-in (len): 4
"""

# ===============================
# Summary:
# Local     → Function ke andar define variable
# Enclosed  → Nested function me outer function ka variable
# Global    → File ke level par define variable
# Built-in  → Python ke predefined names (len, print, etc.)
# ===============================
