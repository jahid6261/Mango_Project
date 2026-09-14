from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.orders.models import OrderStatus


class UpdateOrderStatusRequest(BaseModel):
    status: OrderStatus


class AdminCustomerResponse(BaseModel):
    user_id: int
    name: str
    email: str
    phone: str


class AdminProductResponse(BaseModel):
    product_id: int
    quantity: float


class AdminPaymentResponse(BaseModel):
    method: str
    product_total: float
    delivery_charge: float
    final_price: float


class AdminDeliveryResponse(BaseModel):
    zone: str
    city: str
    postal_code: str
    address: str
    note: Optional[str] = None


class AdminOrderResponse(BaseModel):
    order_id: int

    customer: AdminCustomerResponse
    product: AdminProductResponse
    payment: AdminPaymentResponse
    delivery: AdminDeliveryResponse

    status: OrderStatus
    created_at: datetime
    updated_at: datetime


class AdminAllOrdersResponse(BaseModel):
    success: bool
    total_orders: int
    orders: list[AdminOrderResponse]


class AdminSingleOrderResponse(BaseModel):
    success: bool
    data: AdminOrderResponse