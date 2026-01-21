from pydantic import BaseModel, model_validator


class SignupData(BaseModel):
    # User ka password
    password: str

    # Password confirm karne ke liye
    confirm_password: str

    # =========================
    # Model Validator
    # =========================
    @model_validator(mode="after") # mode="after" likhne ka matlab hai, Pehle saare fields individually validate honge, Phir last me model_validator chalega
    def password_match(cls,self):
        """
        Ye model validator poore object ke validate hone ke baad chalta hai
        Yaha hum password aur confirm_password ko compare karte hain
        """

        # Agar dono passwords same nahi hain → error
        if self.password != self.confirm_password:
            raise ValueError("Password do not match")

        # Agar match ho jaye → self return karna zaroori hai
        return self


data = SignupData(
    password="Admin@123",
    confirm_password="Admin@123"
)

print(data)
# Output: password='Admin@123' confirm_password='Admin@123'