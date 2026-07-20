from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.schemas.cart import AddToCart
from app.core.deps import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Get or Create Cart

def get_or_create_cart(db: Session, user_id: int):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    return cart

#Add to Cart
@router.post("/add")
def add_to_cart(
    data: AddToCart,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    product = db.query(Product).filter(Product.id == data.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock < data.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    cart = get_or_create_cart(db, user_id)

    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == data.product_id
    ).first()

    if item:
        item.quantity += data.quantity
    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=data.product_id,
            quantity=data.quantity
        )
        db.add(item)

    db.commit()

    return {"message": "Item added to cart"}

#View Cart

@router.get("/")
def view_cart(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        return {"items": []}

    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()

    return items


#Update Quantity

@router.put("/update/{item_id}")
def update_quantity(
    item_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    item = db.query(CartItem).filter(CartItem.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.quantity = quantity
    db.commit()

    return {"message": "Cart updated"}


#Remove Item

@router.delete("/remove/{item_id}")
def remove_item(
    item_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    item = db.query(CartItem).filter(CartItem.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    return {"message": "Item removed"}


