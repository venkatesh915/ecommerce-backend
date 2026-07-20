from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.core.admin import get_current_admin


from sqlalchemy import func

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users")
def get_users(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return db.query(User).all()


@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    from fastapi import HTTPException
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user.id == admin.id:
        raise HTTPException(status_code=403, detail="You cannot modify your own role")
        
    if user.id == 1 and role != "admin":
        raise HTTPException(status_code=403, detail="Cannot demote the main admin")
        
    if role not in ["user", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")
        
    user.role = role
    db.commit()
    return {"message": f"User role updated to {role}"}


@router.get("/products")
def get_products(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return db.query(Product).all()


@router.get("/orders")
def get_orders(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return db.query(Order).all()


@router.put("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    from fastapi import HTTPException
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    valid_statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    if status.lower() not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
        
    order.status = status.lower()
    db.commit()
    return {"message": f"Order status updated to {status}"}


@router.get("/sales")
def sales_summary(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    total_orders = db.query(func.count(Order.id)).scalar()

    total_revenue = db.query(func.sum(Order.total_amount)).scalar()

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue or 0
    }