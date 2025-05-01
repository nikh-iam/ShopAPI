from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional
from datetime import datetime

from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.cart import Cart, CartItem
from app.schemas.order_schema import OrderBase

def create_order(db: Session, user_id: int, order: OrderBase) -> Order:
    # Get user's cart
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Calculate total amount
    total_amount = 0
    order_items = []
    
    # Check product availability and calculate total
    for item in cart.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=400, detail=f"Product {item.product_id} not found")
        
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product {product.title}. Available: {product.stock}"
            )
        
        total_amount += product.price * item.quantity
        order_items.append(OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        ))
    
    # Create order
    db_order = Order(
        user_id=user_id,
        shipping_address=order.shipping_address,
        payment_method=order.payment_method,
        total_amount=total_amount,
        items=order_items
    )
    
    # Update product stocks
    for item in cart.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        product.stock -= item.quantity
    
    # Clear cart
    cart.items = []
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id).first()

def get_user_orders(db: Session, user_id: int) -> List[Order]:
    return db.query(Order).filter(Order.user_id == user_id).all()

def update_order_status(db: Session, order_id: int, status: str) -> Optional[Order]:
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        return None
    
    if db_order.status in ["cancelled"]:
        raise HTTPException(
            status_code=400,
            detail="Order cannot be updated as it is cancelled"
        )
    
    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order

def cancel_order(db: Session, order_id: int, user_id: int) -> bool:
    db_order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not db_order:
        return False
    
    if db_order.status not in ["placed", "processing"]:
        raise HTTPException(
            status_code=400,
            detail="Order cannot be cancelled as it's already shipped or delivered"
        )
    
    # Restore product stocks
    for item in db_order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock += item.quantity
    
    db_order.status = "cancelled"
    db.commit()
    return True
