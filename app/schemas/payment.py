from enum import Enum
from pydantic import BaseModel


class PaymentMethod(str, Enum):
    COD = "COD"
    ONLINE = "ONLINE"


class PaymentCreate(BaseModel):
    order_id: int
    payment_method: PaymentMethod


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    payment_method: str
    payment_status: str
    transaction_id: str | None

    class Config:
        from_attributes = True