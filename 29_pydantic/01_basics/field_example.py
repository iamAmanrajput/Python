# BaseModel Pydantic ka core class hai
# Ye automatic data validation aur type conversion karta hai
from pydantic import BaseModel, ValidationError
from typing import List, Dict, Optional


# ================== CART MODEL ==================

class Cart(BaseModel):

    # User ki unique id (integer)
    user_id: int

    # Cart me added item names ki list
    items: List[str]

    # Har item ki quantity
    # key = item name (str)
    # value = quantity (int)
    quantities: Dict[str, int]


# ================== BLOG POST MODEL ==================

class BlogPost(BaseModel):

    # Blog ka title
    title: str

    # Blog ka main content
    content: str

    # Blog image ka URL
    # Optional field hai, default None
    image_url: Optional[str] = None


# ================== TEST CASES ==================

# Test Case 1: Valid Cart data
cart = Cart(
    user_id=1,
    items=["Laptop", "Mouse"],
    quantities={
        "Laptop": 1,
        "Mouse": 2
    }
)

print(cart)

# Output:
# user_id=1 items=['Laptop', 'Mouse'] quantities={'Laptop': 1, 'Mouse': 2}


print("\n----------------------\n")


# Test Case 2: Valid BlogPost data (image_url missing)
blog = BlogPost(
    title="Pydantic Basics",
    content="This blog explains the basics of Pydantic models."
)

print(blog)

# Output:
# title='Pydantic Basics' content='This blog explains the basics of Pydantic models.' image_url=None


print("\n----------------------\n")


# Test Case 3: Invalid data (quantity wrong type)
try:
    bad_cart = Cart(
        user_id=2,
        items=["Keyboard"],
        quantities={
            "Keyboard": "two"   # ❌ int expected
        }
    )
except ValidationError as e:
    print(e)

# Output:
# 1 validation error for Cart
# quantities -> Keyboard
#   value is not a valid integer (type=type_error.integer)
