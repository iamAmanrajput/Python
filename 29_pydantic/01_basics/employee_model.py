from typing import Optional
from pydantic import BaseModel, Field


# =========================
# Employee Model
# =========================
class Employee(BaseModel):
    # id: Employee ka unique identifier
    # Required field hai, integer hona zaroori hai
    id: int

    # name: Employee ka naam
    # ... ka matlab → ye field required hai
    # min_length=3 → naam kam se kam 3 characters ka hona chahiye
    # max_length=50 → naam 50 characters se zyada nahi ho sakta
    # description → API docs (Swagger) me show hota hai
    # examples → sample value dikhane ke liye
    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Employee Name",
        examples=["Hitesh Choudhary"]
    )

    # department: Employee ka department
    # Optional[str] → value aa bhi sakti hai ya nahi bhi
    # Agar value nahi aayi to default "General" set ho jayega
    department: Optional[str] = "General"

    # salary: Employee ki salary
    # gt=0 → salary 0 se zyada honi chahiye
    # Negative ya zero salary allowed nahi hai
    salary: float = Field(
        ...,
        gt=0,
        description="Employee Salary"
    )


# =========================
# User Model
# =========================
class User(BaseModel):
    # email: User ka email address
    # regex → email ka proper format validate karta hai
    # Agar format galat hua to validation error aayega
    email: str = Field(
        ...,
        regex=r"^[\w\.-]+@[\w\.-]+\.\w+$",
        description="User email address"
    )

    # phone: User ka mobile number
    # regex → Indian phone number validate karta hai
    # Number 6-9 se start hona chahiye aur total 10 digits hone chahiye
    phone: str = Field(
        ...,
        regex=r"^[6-9]\d{9}$",
        description="User phone number"
    )

    # age: User ki age
    # ge=0 → age negative nahi ho sakti
    # le=150 → age 150 se zyada nahi ho sakti
    age: int = Field(
        ...,
        ge=0,
        le=150,
        description="Age in years"
    )

    # discount: Discount percentage
    # default=0.0 → agar discount nahi bheja to 0 maan liya jayega
    # ge=0 → discount negative nahi ho sakta
    # le=100 → discount 100% se zyada nahi ho sakta
    discount: float = Field(
        default=0.0,
        ge=0,
        le=100,
        description="Discount percentage"
    )


# =========================
# Example: Employee Object Creation
# =========================

# Input data dictionary
# Note: department nahi diya, isliye default "General" set hoga
input_data = {
    "id": 1,
    "name": "Hitesh Choudhary",
    "salary": 75000.50
}

# Employee object create ho raha hai
employee = Employee(**input_data)

# Validated & parsed data print hoga
print(employee)

# Output:
# id=1 name='Hitesh Choudhary' department='General' salary=75000.5