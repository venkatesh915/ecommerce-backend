from pydantic import BaseModel


class ProductCreate(BaseModel):
    category_id: int
    title: str
    description: str | None = None
    brand: str | None = None
    image_url: str | None = None
    images: list | dict | None = None
    specifications: dict | None = None
    price: float
    stock: int


class ProductOut(BaseModel):
    id: int
    category_id: int
    title: str
    description: str | None
    brand: str | None
    image_url: str | None
    images: list | dict | None = None
    specifications: dict | None = None
    price: float
    stock: int

    class Config:
        from_attributes = True