from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from datetime import datetime
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    category_id = Column(Integer, ForeignKey("categories.id"))

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    brand = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    images = Column(JSON, nullable=True)
    specifications = Column(JSON, nullable=True)

    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    