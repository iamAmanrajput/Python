from pydantic import BaseModel, computed_field


class Product(BaseModel):
    # Price of a single product
    price: float

    # Quantity of the product
    quantity: int

    # computed_field ka use karke derived field banate hain
    # Ye field input me nahi aata, balki runtime pe calculate hota hai
    @computed_field
    @property
    def total_price(self) -> float:
        # Total price = price * quantity
        return self.price * self.quantity


# Product object create kar rahe hain
product = Product(price=499.99, quantity=3)

# Individual fields access
print("Price:", product.price)
print("Quantity:", product.quantity)

# Computed field access
print("Total Price:", product.total_price)

# Model ko dictionary me convert karna
print("Product as dict:", product.model_dump())


# output
# Price: 499.99
# Quantity: 3
# Total Price: 1499.97
# Product as dict: {
#   'price': 499.99,
#   'quantity': 3,
#   'total_price': 1499.97
# }
