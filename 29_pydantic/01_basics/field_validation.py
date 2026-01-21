from pydantic import BaseModel, Field, field_validator


class User(BaseModel):
    # User ki age
    age: int = Field(
        ...,
        ge=0,
        le=120,
        description="User age"
    )

    # Discount percentage
    discount: float = Field(
        default=0,
        ge=0,
        le=100,
        description="Discount percentage"
    )

    # =========================
    # Field Validator
    # =========================
    @field_validator("discount")
    @classmethod
    def validate_discount_based_on_age(cls, discount_value, info):
        """
        Ye validator discount field ke liye chalega,
        lekin age ke basis par decision lega
        """

        age = info.data.get("age")  # age field ki value nikal rahe hain

        # Agar age 18 se kam hai → user allowed nahi
        if age is not None and age < 18:
            raise ValueError("User must be at least 18 years old")

        # Agar age 60 ya usse zyada hai → minimum 20% discount hona chahiye
        if age is not None and age >= 60 and discount_value < 20:
            raise ValueError("Senior citizens must have at least 20% discount")

        # Agar sab sahi hai → discount return kar do
        return discount_value

user = User(age=65, discount=25)
print(user)

# Output: age=65 discount=25.0