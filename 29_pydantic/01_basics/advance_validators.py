from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime


# -----------------------------
# 1️ Person Model
# -----------------------------
class Person(BaseModel):
    # First name of the person
    first_name: str

    # Last name of the person
    last_name: str

    # field_validator ka use karke multiple fields validate kar rahe hain
    # Ye validation tab chalega jab individual field ka value parse ho chuka hoga
    @field_validator('first_name', 'last_name')
    def names_must_be_capitalize(cls, v):
        # Check: name title case me hona chahiye (e.g. "Aman", "Singh")
        if not v.istitle():
            # Agar capitalized nahi hai to error throw hoga
            raise ValueError('Names must be capitalized')
        # Valid value return karna zaroori hota hai
        return v


# -----------------------------
# 2️ User Model
# -----------------------------
class User(BaseModel):
    # Email address of the user
    email: str

    # field_validator email ko normalize karne ke liye
    # Ye input email ko lowercase aur trim karta hai
    @field_validator('email')
    def normalize_email(cls, v):
        # Example: "  TEST@GMAIL.COM  " → "test@gmail.com"
        return v.lower().strip()


# -----------------------------
# 3️ Product Model
# -----------------------------
class Product(BaseModel):
    # Price string format me aata hai (e.g. "$4.44")
    price: str  # "$4.44"

    # mode="before" ka matlab:
    # validation se pehle raw input pe kaam karna
    @field_validator('price', mode='before')
    def parse_price(cls, v):
        # Agar input string hai to "$" hata ke float me convert karte hain
        if isinstance(v, str):
            return float(v.replace('$', ''))
        # Agar already numeric ho to as-it-is return
        return v


# -----------------------------
# 4️ DateRange Model
# -----------------------------
class DateRange(BaseModel):
    # Start date of the range
    start_date: datetime

    # End date of the range
    end_date: datetime

    # model_validator ka use poore model ko validate karne ke liye hota hai
    # mode="after" ka matlab:
    # sab fields validate hone ke baad ye validator chalega
    @model_validator(mode="after")
    def validate_date_range(cls, values):
        # Business rule:
        # end_date hamesha start_date ke baad honi chahiye
        if values.start_date >= values.end_date:
            raise ValueError('end_date must be after start_date')

        # Valid model return karna mandatory hota hai
        return values
