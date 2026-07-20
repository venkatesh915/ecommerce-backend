from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models.user import User

from app.models.category import Category
from app.models.product import Product
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.address import Address 


from app.routers.auth import router as auth_router

from app.routers.category import router as category_router

from app.routers.product import router as product_router

from app.routers.cart import router as cart_router

from app.routers.order import router as order_router

from app.routers.address import router as address_router

from app.routers.payment import router as payment_router

from app.models.payment import Payment

from app.routers.wishlist import router as wishlist_router

from app.routers.review import router as review_router

from app.routers.admin import router as admin_router

from app.routers.user import router as user_router

app = FastAPI(
    title="E-Commerce Backend API",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:5173",  # React frontend
    "http://localhost:5174",  # Alternate React port
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(address_router)
app.include_router(payment_router)
app.include_router(wishlist_router)
app.include_router(review_router)
app.include_router(admin_router)
app.include_router(user_router)


Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "E-Commerce API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}