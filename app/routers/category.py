from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryOut

router = APIRouter(prefix="/categories", tags=["Categories"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Get All Categories

@router.get("/", response_model=list[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


#Create Category

@router.post("/")
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):

    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_cat = Category(
        name=category.name,
        description=category.description
    )

    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)

    return {"message": "Category created successfully"}

#UPDATE CATEGORY

@router.put("/{category_id}")
def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):

    cat = db.query(Category).filter(Category.id == category_id).first()

    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    cat.name = category.name
    cat.description = category.description

    db.commit()

    return {"message": "Category updated successfully"}


#delete

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):

    cat = db.query(Category).filter(Category.id == category_id).first()

    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(cat)
    db.commit()

    return {"message": "Category deleted successfully"}


