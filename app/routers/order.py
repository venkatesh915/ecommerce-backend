from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import uuid

from app.database import SessionLocal

from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem


from app.core.deps import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()






@router.post("/place")
def place_order(
    address_id: int = Query(...),
    payment_method: str = Query("cod"),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()

    if not items:
        raise HTTPException(status_code=400, detail="No items in cart")

    total = 0

    # Calculate total price
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {product.title}"
            )

        total += product.price * item.quantity

    tracking_number = f"TRK-{str(uuid.uuid4())[:8].upper()}"

    # Create Order
    order = Order(
        user_id=user_id,
        address_id=address_id,
        total_amount=total,
        status="confirmed",
        payment_method=payment_method,
        tracking_number=tracking_number
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    # Create Order Items + reduce stock
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )

        product.stock -= item.quantity

        db.add(order_item)

    # Clear cart after order
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()

    db.commit()

    return {
        "message": "Order placed successfully",
        "order_id": order.id,
        "total": total
    }


from app.schemas.order import OrderOut

#Get User Orders

@router.get("/", response_model=list[OrderOut])
def get_orders(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    orders = db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()
    for o in orders:
        o.items = db.query(OrderItem).filter(OrderItem.order_id == o.id).all()
    return orders


#Get Single Order

@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    return order



