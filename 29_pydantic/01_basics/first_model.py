from pydantic import BaseModel
# BaseModel Pydantic ka core class hota hai
# Isse inherit karke hum apna data model banate hain

class User(BaseModel):
    # User model define kar rahe hain
    # Har field ke sath uska data type bataya gaya hai

    id: int          # id integer honi chahiye
    name: str        # name string hona chahiye
    is_active: bool  # is_active sirf True/False accept karega


# Ye input data hai jo normally user, API, ya database se aata hai
input_data = {
    "id": 1,
    "name": "Alice",
    "is_active": True
}

# User(**input_data) ka matlab:
# dictionary ke values ko User model me pass karna
# Pydantic yahan automatically:
# 1. Data validate karega (type sahi hai ya nahi)
# 2. Galat data hoga to error throw karega
# 3. Sahi data hoga to object bana dega

user = User(**input_data)  # id=1, name="Alice", is_active=True

# User object ko print kar rahe hain
# Pydantic readable format me output deta hai
print(user)

# Output:
# id=1 name='Alice' is_active=True