from sqlalchemy import Column, Integer, String, Boolean, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone_no = Column(String(20), nullable=True)
    addresses = Column(JSON, default=[])
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # Relationships
    orders = relationship("Order", back_populates="user")
    cart = relationship("Cart", back_populates="user", uselist=False)
    # addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")


# class Address(Base):
#     __tablename__ = "addresses"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     address = Column(String, nullable=False)
#     is_default = Column(Boolean, default=False)

#     # Relationships
#     user = relationship("User", back_populates="addresses")