from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional, Any, Dict

from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart_schema import CartItemCreate

def calculate_cart_totals(cart: Cart) -> Dict[str, Any]:
    return {
        "total_items": cart.total_items,
        "total_price": cart.total_price
    }

def get_user_cart(db: Session, user_id: int) -> Optional[Dict[str, Any]]:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        return None
    
    totals = calculate_cart_totals(cart)
    return {
        "id": cart.id,
        "user_id": cart.user_id,
        "items": [{
            "id": item.id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "product": {
                "id": item.product.id,
                "title": item.product.title,
                "price": item.product.price
            }
        } for item in cart.items],
        **totals
    }

def add_to_cart(db: Session, user_id: int, item: CartItemCreate) -> dict:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item.product_id
    ).first()

    if existing_item:
        if product.stock < existing_item.quantity + item.quantity:
            raise HTTPException(status_code=400, detail="Not enough stock available")
        existing_item.quantity += item.quantity
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=item.product_id, quantity=item.quantity)
        db.add(cart_item)

    db.commit()
    db.refresh(cart)
    return get_user_cart(db, user_id)

def update_cart_item(db: Session, user_id: int, item_id: int, quantity: int) -> Optional[Cart]:
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        return None
    
    cart_item = next((ci for ci in cart.items if ci.id == item_id), None)
    if not cart_item:
        return None
    
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")
    
    cart_item.quantity = quantity
    db.commit()
    return get_user_cart(db, user_id) 

def remove_from_cart(db: Session, user_id: int, item_id: int) -> Optional[Cart]:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        return None

    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.id == item_id
    ).first()

    if not cart_item:
        return None

    db.delete(cart_item)
    db.commit()
    return get_user_cart(db, user_id)

def clear_cart(db: Session, user_id: int) -> bool:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        return False

    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    return True