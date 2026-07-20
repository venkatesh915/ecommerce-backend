import os
import random
from datetime import datetime
from app.database import SessionLocal, engine, Base
from app.models.category import Category
from app.models.product import Product
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# 20 Categories
CATEGORIES = [
    {"name": "Mobiles", "keyword": "smartphone,mobile", "brands": ["Apple", "Samsung", "OnePlus", "Google", "Xiaomi", "Vivo", "Oppo"]},
    {"name": "Laptops", "keyword": "laptop,macbook", "brands": ["Apple", "Dell", "HP", "Lenovo", "ASUS", "Acer", "MSI"]},
    {"name": "Tablets", "keyword": "ipad,tablet", "brands": ["Apple", "Samsung", "Lenovo", "Microsoft"]},
    {"name": "Televisions", "keyword": "television,smarttv", "brands": ["Sony", "Samsung", "LG", "TCL", "Hisense"]},
    {"name": "Accessories", "keyword": "headphones,earbuds", "brands": ["Sony", "Bose", "Apple", "JBL", "Sennheiser"]},
    {"name": "Fashion", "keyword": "fashion,clothing", "brands": ["Zara", "H&M", "Levi's", "Puma", "Nike"]},
    {"name": "Men's Clothing", "keyword": "menswear,shirt", "brands": ["Peter England", "Raymond", "Allen Solly", "Van Heusen"]},
    {"name": "Women's Clothing", "keyword": "womenswear,dress", "brands": ["Biba", "W", "Aurelia", "FabIndia"]},
    {"name": "Shoes", "keyword": "sneakers,shoes", "brands": ["Nike", "Adidas", "Puma", "Reebok", "New Balance", "Asics"]},
    {"name": "Watches", "keyword": "smartwatch,watch", "brands": ["Apple", "Samsung", "Garmin", "Fossil", "Casio", "Titan"]},
    {"name": "Beauty", "keyword": "makeup,cosmetics", "brands": ["MAC", "L'Oreal", "Maybelline", "Nykaa", "Lakme"]},
    {"name": "Kitchen", "keyword": "kitchen,appliance", "brands": ["Philips", "Prestige", "Bajaj", "Morphy Richards", "Bosch"]},
    {"name": "Home Decor", "keyword": "homedecor,vase", "brands": ["Home Centre", "IKEA", "Chumbak", "FabIndia"]},
    {"name": "Furniture", "keyword": "furniture,sofa", "brands": ["IKEA", "Pepperfry", "Urban Ladder", "Godrej Interio"]},
    {"name": "Sports", "keyword": "sports,fitness", "brands": ["Decathlon", "Nivia", "Yonex", "Cosco", "Wilson"]},
    {"name": "Books", "keyword": "book,novel", "brands": ["Penguin", "HarperCollins", "Rupa", "Arihant"]},
    {"name": "Toys", "keyword": "toys,lego", "brands": ["LEGO", "Hot Wheels", "Barbie", "Fisher-Price", "Hasbro"]},
    {"name": "Grocery", "keyword": "groceries,vegetables", "brands": ["Tata Sampann", "Aashirvaad", "Fortune", "Nestle"]},
    {"name": "Health", "keyword": "vitamins,supplements", "brands": ["Optimum Nutrition", "MuscleBlaze", "Himalaya", "Dabur"]},
    {"name": "Automotive", "keyword": "caraccessories,helmet", "brands": ["Studds", "Vega", "Steelbird", "Michelin", "Bosch"]}
]

def generate_product_name(category, brand):
    suffixes = {
        "Mobiles": ["Pro", "Max", "Ultra", "Lite", "Plus", "5G", "SE", "Note"],
        "Laptops": ["Pro", "Air", "XPS", "ThinkPad", "ZenBook", "Pavilion", "Envy"],
        "Tablets": ["Pro", "Air", "Mini", "Tab S", "Surface", "MatePad"],
        "Televisions": ["OLED 4K", "QLED 8K", "Smart LED", "Crystal 4K", "Bravia XR"],
        "Accessories": ["Wireless Earbuds", "Noise Cancelling Headphones", "Bluetooth Speaker", "Power Bank 20000mAh", "Fast Charger 65W"],
        "Fashion": ["Premium Jacket", "Denim Jeans", "Cotton T-Shirt", "Summer Collection", "Winter Coat"],
        "Men's Clothing": ["Formal Shirt", "Chinos", "Polo T-Shirt", "Blazer", "Track Pants"],
        "Women's Clothing": ["Floral Dress", "Kurti", "Silk Saree", "Palazzo Set", "Tops"],
        "Shoes": ["Running Shoes", "Sneakers", "Walking Shoes", "Sports Trainers", "Formal Leather Shoes"],
        "Watches": ["Smartwatch Series", "Chronograph", "Analog Watch", "Digital Sports Watch", "Fitness Band"],
        "Beauty": ["Matte Lipstick", "Foundation", "Mascara", "Eyeshadow Palette", "Face Serum"],
        "Kitchen": ["Mixer Grinder", "Air Fryer", "Microwave Oven", "Induction Cooktop", "Electric Kettle"],
        "Home Decor": ["Wall Art", "Ceramic Vase", "Scented Candles", "Table Lamp", "Cushion Covers"],
        "Furniture": ["3-Seater Sofa", "Queen Size Bed", "Office Chair", "Dining Table Set", "Bookshelf"],
        "Sports": ["Tennis Racket", "Football", "Yoga Mat", "Dumbbells Set", "Cricket Bat"],
        "Books": ["Best Seller Novel", "Biography", "Self-Help Book", "Science Fiction", "Cookbook"],
        "Toys": ["Building Blocks", "Action Figure", "Remote Control Car", "Board Game", "Plush Toy"],
        "Grocery": ["Premium Tea", "Coffee Powder", "Basmati Rice 5kg", "Olive Oil 1L", "Almonds 500g"],
        "Health": ["Whey Protein", "Multivitamin Tablets", "Omega 3 Capsules", "Herbal Supplement", "Protein Bar"],
        "Automotive": ["Full Face Helmet", "Car Polish", "Microfiber Cloth", "Dash Cam", "Tire Inflator"]
    }
    
    prefix = random.choice(["", "New ", "Premium ", "Advanced "])
    suffix = random.choice(suffixes.get(category, ["Pro", "Max", "Edition"]))
    model = random.randint(1, 99) if category in ["Mobiles", "Laptops", "Tablets", "Watches"] else ""
    
    return f"{brand} {suffix} {model}".strip()

def seed_database():
    db = SessionLocal()

    print("Dropping and recreating all tables...")
    from sqlalchemy import text
    with engine.connect() as con:
        con.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))
        con.commit()
    Base.metadata.create_all(bind=engine)

    print("Creating admin user...")
    admin_user = User(
        email="venky@gmail.com",
        full_name="Venky Admin",
        password=get_password_hash("123456"),
        role="admin"
    )
    db.add(admin_user)
    
    test_user = User(
        email="user@example.com",
        full_name="Test User",
        password=get_password_hash("user123"),
        role="customer"
    )
    db.add(test_user)
    db.commit()

    print("Seeding Categories...")
    category_map = {}
    
    # We will use LoremFlickr with category keywords to ensure unique, relevant images.
    # To prevent any image caching issues and ensure extreme uniqueness, we use a global counter for locks.
    global_img_counter = 1000
    
    for cat_data in CATEGORIES:
        global_img_counter += 1
        new_cat = Category(
            name=cat_data["name"], 
            description=f"Premium {cat_data['name']} on BharatBazaar", 
            image_url=f"https://loremflickr.com/600/600/{cat_data['keyword']}?lock={global_img_counter}"
        )
        db.add(new_cat)
        db.commit()
        db.refresh(new_cat)
        category_map[cat_data["name"]] = new_cat.id

    print("Generating 600 Realistic Products...")
    all_products = []
    
    for cat_data in CATEGORIES:
        cat_id = category_map[cat_data["name"]]
        
        for i in range(30):
            global_img_counter += 1
            brand = random.choice(cat_data["brands"])
            title = generate_product_name(cat_data["name"], brand)
            
            # Base pricing logic based on category
            base_price = 1000
            if cat_data["name"] in ["Mobiles", "Laptops", "Televisions"]:
                base_price = random.randint(15000, 150000)
            elif cat_data["name"] in ["Tablets", "Watches", "Furniture"]:
                base_price = random.randint(5000, 50000)
            elif cat_data["name"] in ["Grocery", "Books", "Beauty"]:
                base_price = random.randint(150, 2500)
            else:
                base_price = random.randint(500, 10000)
                
            # Generate 4 unique images per product
            images = [
                f"https://loremflickr.com/600/600/{cat_data['keyword']}?lock={global_img_counter + 1}",
                f"https://loremflickr.com/600/600/{cat_data['keyword']}?lock={global_img_counter + 2}",
                f"https://loremflickr.com/600/600/{cat_data['keyword']}?lock={global_img_counter + 3}",
                f"https://loremflickr.com/600/600/{cat_data['keyword']}?lock={global_img_counter + 4}"
            ]
            global_img_counter += 4
            
            specs = {
                "Brand": brand,
                "Model": title,
                "Category": cat_data["name"],
                "Release Year": "2024",
                "Warranty": "1 Year Manufacturer Warranty"
            }

            all_products.append(Product(
                category_id=cat_id, 
                title=title, 
                description=f"Experience the best in class {cat_data['name'].lower()} with the new {title} by {brand}. Designed to offer unparalleled performance, premium build quality, and extreme reliability. Perfect for daily use.", 
                brand=brand, 
                image_url=images[0], 
                images=images, 
                specifications=specs, 
                price=base_price, 
                stock=random.randint(0, 150)
            ))

    # Batch insert in chunks of 100 to avoid memory issues
    for i in range(0, len(all_products), 100):
        db.add_all(all_products[i:i+100])
        db.commit()
        print(f"Inserted {i+100} products...")
        
    print(f"Successfully generated {len(all_products)} products.")
    db.close()

if __name__ == "__main__":
    seed_database()
