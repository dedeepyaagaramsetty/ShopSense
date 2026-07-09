from app.database.database import SessionLocal
from app.models.admin import Admin

db = SessionLocal()

admin = Admin(
    full_name="Super Admin",
    email="admin@shopsense.com",
    password="admin123"
)

db.add(admin)
db.commit()
db.close()

print("Admin created successfully!")