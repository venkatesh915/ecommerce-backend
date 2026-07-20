from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.address import Address
from app.core.deps import get_current_user
from pydantic import BaseModel

from app.schemas.address import AddressCreate,AddressOut,AddressUpdate



router = APIRouter(prefix="/address", tags=["Address"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class AddressCreate(BaseModel):
    full_name: str
    phone: str
    address: str
    city: str
    state: str
    pincode: str


@router.post("/")
def create_address(
    data: AddressCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    new_address = Address(
        user_id=user_id,
        full_name=data.full_name,
        phone=data.phone,
        address=data.address,
        city=data.city,
        state=data.state,
        pincode=data.pincode
    )

    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    return {
        "message": "Address created",
        "address_id": new_address.id
    }


#get all address

@router.get("/", response_model=list[AddressOut])
def get_addresses(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return db.query(Address).filter(
        Address.user_id == user_id
    ).all()

#Update Address

@router.put("/{address_id}")
def update_address(
    address_id: int,
    data: AddressUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == user_id
    ).first()

    if not address:
        raise HTTPException(404, "Address not found")

    for key, value in data.model_dump().items():
        setattr(address, key, value)

    db.commit()

    return {"message": "Address updated"}


#Delete Address


@router.delete("/{address_id}")
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == user_id
    ).first()

    if not address:
        raise HTTPException(404, "Address not found")

    db.delete(address)
    db.commit()

    return {"message": "Address deleted"}

#Set Default Address

@router.put("/default/{address_id}")
def set_default_address(
    address_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    db.query(Address).filter(
        Address.user_id == user_id
    ).update({"is_default": False})

    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == user_id
    ).first()

    if not address:
        raise HTTPException(404, "Address not found")

    address.is_default = True

    db.commit()

    return {"message": "Default address updated"}


