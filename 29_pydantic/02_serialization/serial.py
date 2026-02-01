from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict


# Address model (nested model)
class Address(BaseModel):
    street: str
    city: str
    zip_code: str


# User model
class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True           # Default value
    createdAt: datetime              # datetime field
    address: Address                 # Nested Pydantic model
    tags: List[str] = []             # List field (mutable default – generally avoid)

    # Custom JSON encoder for datetime
    # Jab model JSON me convert hoga, datetime is format me dikhega
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.strftime('%d-%m-%Y %H:%M:%S')
        }
    )


# Creating User object
user = User(
    id=1,
    name="Hitesh",
    email="h@hitesh.ai",
    createdAt=datetime(2024, 3, 15, 14, 30),
    address=Address(
        street="Something",
        city="Jaipur",
        zip_code="009988"
    ),
    is_active=False,
    tags=["premium", "subscriber"]
)


# Convert Pydantic model to Python dictionary
python_dict = user.model_dump()
print(python_dict)

# OUTPUT:
# {
#   'id': 1,
#   'name': 'Hitesh',
#   'email': 'h@hitesh.ai',
#   'is_active': False,
#   'createdAt': datetime.datetime(2024, 3, 15, 14, 30),
#   'address': {
#       'street': 'Something',
#       'city': 'Jaipur',
#       'zip_code': '009988'
#   },
#   'tags': ['premium', 'subscriber']
# }


# Printing the model directly (human-readable form)
print(user)

# OUTPUT:
# id=1 name='Hitesh' email='h@hitesh.ai' is_active=False
# createdAt=datetime.datetime(2024, 3, 15, 14, 30)
# address=Address(street='Something', city='Jaipur', zip_code='009988')
# tags=['premium', 'subscriber']


# Convert model to JSON encoded string
json_str = user.model_dump_json()
print(json_str)

# OUTPUT (JSON encoded string):
# {
#   "id":1,
#   "name":"Hitesh",
#   "email":"h@hitesh.ai",
#   "is_active":false,
#   "createdAt":"15-03-2024 14:30:00",
#   "address":{
#       "street":"Something",
#       "city":"Jaipur",
#       "zip_code":"009988"
#   },
#   "tags":["premium","subscriber"]
# }
