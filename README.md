# BharatBazaar E-Commerce Backend 🛒

Backend API for **BharatBazaar**, a full-stack e-commerce application built using **FastAPI, SQLAlchemy, PostgreSQL, and JWT Authentication**.

This backend provides REST APIs for users, products, categories, carts, orders, payments, reviews, wishlist, addresses, and admin operations.

---

# 🌐 Live Application

Frontend:
```
https://ecommerce-frontend-kohl-two.vercel.app/
```

Backend API:
```
https://ecommerce-backend-production-b444.up.railway.app
```

API Documentation:

```
https://ecommerce-backend-production-b444.up.railway.app/docs
```

---

# 🚀 Features

## Authentication & Users

✅ User Registration  
✅ User Login  
✅ JWT Access Token Authentication  
✅ Password Hashing  
✅ User Profile  
✅ Role Based Access (User/Admin)


## Product Management

✅ Create Products  
✅ Update Products  
✅ Delete Products  
✅ Product Listing  
✅ Product Search  
✅ Category Based Filtering  
✅ Product Details


## Category Management

✅ Create Categories  
✅ Update Categories  
✅ Delete Categories  
✅ Category Listing


## Cart System

✅ Add Product To Cart  
✅ Update Quantity  
✅ Remove Cart Items  
✅ View Cart Total


## Order System

✅ Create Orders  
✅ Order History  
✅ Order Status Management  
✅ Order Items Tracking


## Address Management

✅ Add Address  
✅ Update Address  
✅ Delete Address  
✅ User Delivery Addresses


## Payment

✅ Payment API Integration  
✅ Payment Records


## Wishlist

✅ Add Wishlist Products  
✅ Remove Wishlist Products  
✅ View Wishlist


## Reviews

✅ Product Reviews  
✅ User Ratings  
✅ Review Management


## Admin Features

✅ Admin Dashboard  
✅ Product Management  
✅ Category Management  
✅ Order Management  
✅ User Management

---

# 🛠️ Tech Stack

## Backend

- Python 3.11+
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Pydantic
- JWT Authentication
- Passlib / Bcrypt
- Uvicorn


## Deployment

- Railway


---

# 📂 Project Structure

```
backend/
│
├── app/
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   └── payment.py
│   │
│   ├── schemas/
│   │   ├── user_schema.py
│   │   ├── product_schema.py
│   │   └── order_schema.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   ├── payment.py
│   │   ├── wishlist.py
│   │   └── admin.py
│   │
│   ├── services/
│   │   ├── auth.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   ├── payment.py
│   │   ├── wishlist.py
│   │   └── admin.py
│   │
│   ├── database.py
│   └── main.py
│
├── requirements.txt
├── .env
├── Dockerfile
└── README.md

```

---

# ⚙️ Installation

Clone repository:

```bash
git clone <your-backend-repository-url>
```

Go to backend folder:

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create:

```
.env
```

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce

JWT_SECRET_KEY=your_secret_key

JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

FRONTEND_URL=https://ecommerce-frontend-kohl-two.vercel.app
```

---

# 🗄️ Database Setup

Create PostgreSQL database:

```
ecommerce
```

Run application.

Tables will be created automatically:

```python
Base.metadata.create_all(bind=engine)
```

---

# ▶️ Run Backend Locally

Start FastAPI server:

```bash
uvicorn app.main:app --reload
```

Server:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

# 🔌 API Routes

## Authentication

```
POST   /register
POST   /login
POST   /logout
```

---

## Products

```
GET    /products
GET    /products/{id}
POST   /products
PUT    /products/{id}
DELETE /products/{id}
```

---

## Categories

```
GET    /categories
POST   /categories
PUT    /categories/{id}
DELETE /categories/{id}
```

---

## Cart

```
GET    /cart
POST   /cart
PUT    /cart/{id}
DELETE /cart/{id}
```

---

## Orders

```
POST /orders
GET  /orders
GET  /orders/{id}
```

---

# 🔒 Security

Implemented:

✅ JWT Authentication  
✅ Password Encryption  
✅ Protected Routes  
✅ Role Based Authorization  
✅ CORS Configuration  
✅ Environment Variables


---

# 🚀 Deployment

Backend deployed using:

```
Railway
```

Deployment URL:

```
https://ecommerce-backend-production-b444.up.railway.app
```

Frontend communicates with backend using:

```
VITE_API_URL
```

---

# 🔄 Frontend Connection

Frontend:

```
https://ecommerce-frontend-kohl-two.vercel.app
```

Backend:

```
https://ecommerce-backend-production-b444.up.railway.app
```

CORS configured to allow frontend requests.

---

# 👨‍💻 Developer

**Venky**

BharatBazaar E-Commerce Platform


---

# 📄 License

This project is developed for learning and portfolio purposes.
