from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.payment import Payment
from app.models.order import Order
from app.schemas.payment import PaymentCreate
from app.core.deps import get_current_user

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Payment
@router.post("/")
def create_payment(
    data: PaymentCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    # Check Order
    order = db.query(Order).filter(
        Order.id == data.order_id,
        Order.user_id == user_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    # Check Existing Payment
    existing_payment = db.query(Payment).filter(
        Payment.order_id == order.id
    ).first()

    if existing_payment:
        raise HTTPException(
            status_code=400,
            detail="Payment already exists for this order"
        )

    # COD Payment
    if data.payment_method == "COD":

        payment = Payment(
            order_id=order.id,
            amount=order.total_amount,
            payment_method="COD",
            payment_status="Pending",
            transaction_id=None
        )

        order.status = "Confirmed"

        db.add(payment)
        db.commit()
        db.refresh(payment)

        return {
            "message": "Cash on Delivery selected",
            "payment": payment
        }

    # Online Payment (Simulation)
    elif data.payment_method == "ONLINE":

        payment = Payment(
            order_id=order.id,
            amount=order.total_amount,
            payment_method="ONLINE",
            payment_status="Success",
            transaction_id="TXN123456789"
        )

        order.status = "Paid"

        db.add(payment)
        db.commit()
        db.refresh(payment)

        return {
            "message": "Payment Successful",
            "payment": payment
        }

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid payment method"
        )


# Get Payment by Order
@router.get("/order/{order_id}")
def get_payment_by_order(
    order_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    payment = db.query(Payment).filter(
        Payment.order_id == order.id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment


# Get Single Payment
@router.get("/{payment_id}")
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    order = db.query(Order).filter(
        Order.id == payment.order_id,
        Order.user_id == user_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized"
        )

    return payment