from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from datetime import datetime
from app.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)

    order_id = Column(Integer, ForeignKey("orders.id"))

    amount = Column(Float)

    payment_method = Column(String)

    payment_status = Column(String, default="pending")

    transaction_id = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)