# BaseModel ko pydantic se import kar rahe hain
# BaseModel data validation aur type checking karta hai
from pydantic import BaseModel, ValidationError


# Product naam ka data model
# Ye mostly API request/response validation ke liye use hota hai
class Product(BaseModel):

    # Product ki unique id (integer honi chahiye)
    id: int

    # Product ka naam (string)
    name: str

    # Product ki price (float)
    price: float

    # Product stock me available hai ya nahi
    # Default value True hai
    in_stock: bool = True


# ================== TEST CASES ==================

# Test Case 1: Correct data
product1 = Product(
    id=101,
    name="Mobile",
    price=15000.75
)

print(product1)

# Output:
# id=101 name='Mobile' price=15000.75 in_stock=True


print("\n----------------------\n")


# Test Case 2: Wrong data type (id string hai)
try:
    product2 = Product(
        id="one",          # invalid type
        name="Laptop",
        price=55000
    )
except ValidationError as e:
    print(e)

# Output:
# 1 validation error for Product
# id
#   value is not a valid integer (type=type_error.integer)
