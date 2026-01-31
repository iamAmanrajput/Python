from typing import Optional, List, Union
from pydantic import BaseModel

# -----------------------------
# Basic Nested Models
# -----------------------------

class Address(BaseModel):
    """
    Address model represents a physical location.
    This is a simple nested model used inside other models.
    """
    street: str            # Street name / house number
    city: str              # City name
    postal_code: str       # Postal / ZIP code


class Company(BaseModel):
    """
    Company model.
    - `address` is optional because a company may not have a registered address yet.
    """
    name: str
    address: Optional[Address] = None


class Employee(BaseModel):
    """
    Employee model.
    - `company` is optional because an employee may be unemployed or freelance.
    """
    name: str
    company: Optional[Company] = None


# -----------------------------
# Mixed Data Types (Union)
# -----------------------------

class TextContent(BaseModel):
    """
    Represents a text-based section in an article.
    """
    type: str = "text"      # Discriminator field to identify content type # default value
    content: str           # Actual text content


class ImageContent(BaseModel):
    """
    Represents an image-based section in an article.
    """
    type: str = "image"    # Discriminator field
    url: str               # Image URL
    alt_text: str          # Alternative text for accessibility


class Article(BaseModel):
    """
    Article model demonstrating the use of Union.
    - `sections` can contain both text and image content.
    """
    title: str
    sections: List[Union[TextContent, ImageContent]]


# -----------------------------
# Deeply Nested Structure
# -----------------------------

class Country(BaseModel):
    """
    Country model.
    """
    name: str              # Country name
    code: str              # ISO country code (e.g., IN, US)


class State(BaseModel):
    """
    State model.
    - Each state belongs to a country.
    """
    name: str
    country: Country


class City(BaseModel):
    """
    City model.
    - Each city belongs to a state.
    """
    name: str
    state: State


class Address(BaseModel):
    """
    Address model with deep nesting.
    - City → State → Country hierarchy.
    """
    street: str
    city: City
    postal_code: str


class Organization(BaseModel):
    """
    Organization model.
    - `head_quarter` is a single address.
    - `branches` is a list of addresses.
    
     Note:
    Using `= []` is allowed but not recommended.
    Best practice is to use `default_factory=list`.
    """
    name: str
    head_quarter: Address
    branches: List[Address] = []  # Prefer: Field(default_factory=list)
