from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.review import Review
from app.models.product import Product
from app.schemas.review import ReviewCreate
from app.core.deps import get_current_user
from fastapi import APIRouter


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def add_review(
    data: ReviewCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    # check product exists
    product = db.query(Product).filter(Product.id == data.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # validate rating
    if data.rating < 1 or data.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be 1-5")

    review = Review(
        user_id=user_id,
        product_id=data.product_id,
        rating=data.rating,
        comment=data.comment
    )

    db.add(review)
    db.commit()

    return {"message": "Review added"}


@router.get("/product/{product_id}")
def get_reviews(
    product_id: int,
    db: Session = Depends(get_db)
):

    reviews = db.query(Review).filter(
        Review.product_id == product_id
    ).all()

    return reviews



from sqlalchemy import func


@router.get("/product/{product_id}/rating")
def get_average_rating(
    product_id: int,
    db: Session = Depends(get_db)
):

    avg = db.query(func.avg(Review.rating)).filter(
        Review.product_id == product_id
    ).scalar()

    return {
        "product_id": product_id,
        "average_rating": round(avg or 0, 2)
    }