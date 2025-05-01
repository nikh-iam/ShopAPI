from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy.orm import Session
from app.core.config import settings

def init_admin_user(db: Session):
    admin_email = settings.ADMIN_EMAIL
    admin_password = settings.ADMIN_PASSWORD
    
    existing_admin = db.query(User).filter(User.email == admin_email).first()
    
    if not existing_admin:
        admin_user = User(
            first_name="Admin",
            last_name="User",
            email=admin_email,
            phone_no=None,
            hashed_password=get_password_hash(admin_password),
            is_active=True,
            is_admin=True,
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("[INFO] Default admin user created")
    else:
        print("[INFO] Admin user already exists")
