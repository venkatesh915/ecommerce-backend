from app.database import engine
from sqlalchemy import text

def migrate():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE orders ADD COLUMN payment_method VARCHAR DEFAULT 'cod'"))
            print("Added payment_method column.")
        except Exception as e:
            print(f"payment_method probably already exists: {e}")
            
        try:
            conn.execute(text("ALTER TABLE orders ADD COLUMN tracking_number VARCHAR"))
            print("Added tracking_number column.")
        except Exception as e:
            print(f"tracking_number probably already exists: {e}")
            
        conn.commit()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
