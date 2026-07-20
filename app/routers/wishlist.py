from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.wishlist import Wishlist
from app.models.product import Product
from app.core.deps import get_current_user
from app.schemas.wishlist import WishlistCreate

from app.models.cart import Cart
from app.models.cart_item import CartItem


router = APIRouter(
    prefix="/wishlist",
    tags=["Wishlist"]
)


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_or_create_cart(db: Session, user_id: int):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    return cart


# ADD TO WISHLIST
@router.post("/")
def add_to_wishlist(
    data: WishlistCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    # check product exists
    product = db.query(Product).filter(Product.id == data.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # prevent duplicates
    existing = db.query(Wishlist).filter(
        Wishlist.user_id == user_id,
        Wishlist.product_id == data.product_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already in wishlist")

    item = Wishlist(
        user_id=user_id,
        product_id=data.product_id
    )

    db.add(item)
    db.commit()

    return {"message": "Added to wishlist"}


# GET WISHLIST
@router.get("/")
def get_wishlist(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    items = db.query(Wishlist).filter(
        Wishlist.user_id == user_id
    ).all()

    return items


# DELETE FROM WISHLIST
@router.delete("/{wishlist_id}")
def remove_from_wishlist(
    wishlist_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    item = db.query(Wishlist).filter(
        Wishlist.id == wishlist_id,
        Wishlist.user_id == user_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    return {"message": "Removed from wishlist"}


@router.post("/move-to-cart/{wishlist_id}")
def move_to_cart(
    wishlist_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    # 1. Get wishlist item
    item = db.query(Wishlist).filter(
        Wishlist.id == wishlist_id,
        Wishlist.user_id == user_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Wishlist item not found")

    # 2. Validate product exists
    product = db.query(Product).filter(Product.id == item.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # 3. Get or create cart
    cart = get_or_create_cart(db, user_id)

    # 4. Check if product already in cart
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item.product_id
    ).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item.product_id,
            quantity=1
        )
        db.add(cart_item)

    # 5. Remove from wishlist
    db.delete(item)

    db.commit()

    return {
        "message": "Moved to cart successfully",
        "product_id": item.product_id
    }