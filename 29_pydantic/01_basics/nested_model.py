from typing import List, Optional
from pydantic import BaseModel


# -------------------------------
# Address Model (Nested Model)
# -------------------------------
# Ye model address ka structure define karta hai
# Isme street, city aur postal_code required hain
class Address(BaseModel):
    street: str
    city: str
    postal_code: str


# -------------------------------
# User Model
# -------------------------------
# User ke andar ek Address object bhi hai
# address field ek nested model hai
class User(BaseModel):
    id: int
    name: str
    address: Address


# -------------------------------
# 1️ Direct Address object bana ke User me pass karna
# -------------------------------
address = Address(
    street="123 something",
    city="Jaipur",
    postal_code="100001"
)

# Yahan hum Address ka object directly User ko de rahe hain
user = User(
    id=1,
    name="Hitesh",
    address=address,
)


# -------------------------------
# 2️ Dict ke through Nested Data pass karna
# -------------------------------
# Yahan address ek normal dictionary hai
# Pydantic automatically ise Address model me convert kar dega
user_data = {
    "id": 1,
    "name": "Hitesh",
    "address": {
        "street": "321 something",
        "city": "Paris",
        "postal_code": "20002"
    }
}

# **user_data ko unpack karke User model me pass kiya
user = User(**user_data)

# Final validated output print
print(user)


# output
# id=1 name='Hitesh' address=Address(street='321 something', city='Paris', postal_code='20002')
