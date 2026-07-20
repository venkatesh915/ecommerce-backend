from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductOut

router = APIRouter(prefix="/products", tags=["Products"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#get all product

@router.get("/", response_model=list[ProductOut])
def get_products(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return db.query(Product).offset(skip).limit(limit).all()


#Search Products
@router.get("/search/", response_model=list[ProductOut])
def search_products(
    q: str = Query("", description="Search query"),
    db: Session = Depends(get_db)
):
    return db.query(Product).filter(
        Product.title.ilike(f"%{q}%")
    ).all()


#get product by id
@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

#Filter by Category

@router.get("/category/{category_id}")
def get_by_category(category_id: int, db: Session = Depends(get_db)):

    return db.query(Product).filter(
        Product.category_id == category_id
    ).all()




#admin apis
#Create Product

@router.post("/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):

    new_product = Product(
        category_id=product.category_id,
        title=product.title,
        description=product.description,
        brand=product.brand,
        image_url=product.image_url,
        price=product.price,
        stock=product.stock
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {"message": "Product created successfully"}

#Update Product

@router.put("/{product_id}")
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):

    db_product = db.query(Product).filter(Product.id == product_id).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.dict().items():
        setattr(db_product, key, value)

    db.commit()

    return {"message": "Product updated successfully"}

#Delete Product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}


