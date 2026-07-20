from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from datetime import datetime
from app.database import Base





class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    address_id = Column(Integer, ForeignKey("addresses.id"))

    total_amount = Column(Float, nullable=False)

    status = Column(String, default="pending")  
    payment_method = Column(String, default="cod")
    tracking_number = Column(String, nullable=True)
    estimated_delivery_time = Column(DateTime, nullable=True)
    destination_distance = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)