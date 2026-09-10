from pydantic import BaseModel, Field
from typing import Optional


class CheckoutSchema(BaseModel):
    product_id: int

    quantity: float = Field(
        gt=0,
        description="Quantity in kilograms (e.g. 0.5 = 500g, 1 = 1kg, 2.5 = 2.5kg)"
    )

    full_name: str
    email: str
    phone_number: str

    city: str
    postal_code: str
    address: str

    note: Optional[str] = None


class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: float

    total_price: float
    delivery_charge: float
    final_price: float

    status: str

    full_name: str
    email: str
    phone_number: str
    city: str
    postal_code: str
    address: str
    note: Optional[str] = None