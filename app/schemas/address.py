from pydantic import BaseModel

class AddressCreate(BaseModel):
    full_name: str
    phone: str
    address: str
    city: str
    state: str
    pincode: str


class AddressUpdate(AddressCreate):
    pass


class AddressOut(AddressCreate):
    id: int
    is_default: bool

    class Config:
        from_attributes = True