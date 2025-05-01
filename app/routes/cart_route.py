from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.cart_schema import CartOut, CartItemCreate
from app.services.cart_service import (
    get_user_cart,
    add_to_cart,
    update_cart_item,
    remove_from_cart,
    clear_cart
)

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/", response_model=CartOut)
def read_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    cart = get_user_cart(db, current_user.id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@router.post("/add", response_model=CartOut)
def add_item_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return add_to_cart(db, current_user.id, item)

@router.put("/update/{item_id}", response_model=CartOut)
def update_cart_item_route(
    item_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    updated_cart = update_cart_item(db, current_user.id, item_id, quantity)
    if not updated_cart:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return updated_cart

@router.delete("/remove/{item_id}", response_model=CartOut)
def remove_item_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    updated_cart = remove_from_cart(db, current_user.id, item_id)
    if not updated_cart:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return updated_cart

@router.delete("/clear", status_code=status.HTTP_204_NO_CONTENT)
def clear_user_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    success = clear_cart(db, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart not found")
    return