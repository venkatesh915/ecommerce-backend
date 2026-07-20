from pydantic import BaseModel
from datetime import datetime


class OrderProductOut(BaseModel):
    id: int
    title: str
    image_url: str | None
    price: float

    class Config:
        from_attributes = True

class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float
    product: OrderProductOut | None = None

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    total_amount: float
    status: str
    payment_method: str
    tracking_number: str | None
    estimated_delivery_time: datetime | None = None
    destination_distance: float | None = None
    address_id: int
    items: list[OrderItemOut] = []

    class Config:
        from_attributes = True