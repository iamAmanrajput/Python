# ============================
# NEW WAY (with – automatic close)
# ============================

#  1. WRITE (overwrite)
with open("orders.txt", "w") as file:
    file.write("Masala Chai – 2 cups\n")


#  2. APPEND (add data)
with open("orders.txt", "a") as file:
    file.write("Ginger Tea – 4 cups\n")


#  3. READ (read data)
with open("orders.txt", "r") as file:
    data = file.read()
    print("NEW WAY OUTPUT:\n", data)


# NEW WAY OUTPUT:
#  Masala Chai – 2 cups
# Ginger Tea – 4 cups
