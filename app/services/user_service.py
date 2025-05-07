from app.models.order import Order
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional, List
from datetime import datetime, timedelta

from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.core.config import settings

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[Order]:
    return db.query(Order).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    # Check if user already exists
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = get_password_hash(user.password)
    
    # Create user
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_no=user.phone_no,
        hashed_password=hashed_password,
        is_active=True,
        is_admin=False,
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def update_user(
    db: Session, 
    user_id: int, 
    user_update: UserUpdate,
    current_user: User
) -> User:
    # Only allow users to update their own profile unless they're admin
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
    
    db_user = get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update user fields
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int, current_user: User) -> bool:
    # Prevent users from deleting themselves unless they're admin
    if user_id == current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot delete your own account"
        )
    
    db_user = get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(db_user)
    db.commit()
    return True

# def get_user_addresses(db: Session, user_id: int) -> List[Address]:
#     return db.query(Address).filter(Address.user_id == user_id).all()

# def get_address_by_id(db: Session, address_id: int, user_id: int) -> Optional[Address]:
#     return db.query(Address).filter(
#         Address.id == address_id, Address.user_id == user_id
#     ).first()

# def create_address(db: Session, user_id: int, address_create: AddressCreate) -> Address:
#     if address_create.is_default:
#         db.query(Address).filter(
#             Address.user_id == user_id, Address.is_default == True
#         ).update({"is_default": False})
    
#     db_address = Address(
#         **address_create.dict(),
#         user_id=user_id,
#     )
#     db.add(db_address)
#     db.commit()
#     db.refresh(db_address)
#     return db_address

# def update_address(db: Session, address_id: int, user_id: int, address_update: AddressUpdate) -> Address:
#     db_address = get_address_by_id(db, address_id, user_id)
#     if not db_address:
#         raise HTTPException(status_code=404, detail="Address not found")

#     update_data = address_update.dict(exclude_unset=True)

#     if "is_default" in update_data and update_data["is_default"]:
#         db.query(Address).filter(
#             Address.user_id == user_id, Address.is_default == True
#         ).update({"is_default": False})
    
#     for field, value in update_data.items():
#         setattr(db_address, field, value)
    
#     db.commit()
#     db.refresh(db_address)
#     return db_address

# def delete_address(db: Session, address_id: int, user_id: int) -> bool:
#     db_address = get_address_by_id(db, address_id, user_id)
#     if not db_address:
#         raise HTTPException(status_code=404, detail="Address not found")
    
#     db.delete(db_address)
#     db.commit()
#     return True