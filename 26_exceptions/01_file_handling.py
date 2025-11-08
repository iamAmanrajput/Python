# ============================
# OLD WAY (Manual File Handling)
# ============================

#  1. WRITE (overwrite)
file = open("order.txt", "w")
try:
    file.write("Masala Chai – 2 cups\n")
finally:
    file.close()


#  2. APPEND (add new data)
file = open("order.txt", "a")
try:
    file.write("Ginger Tea – 4 cups\n")
finally:
    file.close()


#  3. READ (read file content)
file = open("order.txt", "r")
try:
    data = file.read()
    print("OLD WAY OUTPUT:\n", data)
finally:
    file.close()


# OLD WAY OUTPUT:
#  Masala Chai – 2 cups
# Ginger Tea – 4 cups
