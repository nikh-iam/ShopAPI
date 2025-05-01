from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.order_schema import (
    OrderBase,
    OrderOut,
    OrderStatusUpdate
)
from app.services.order_service import (
    create_order,
    get_order,
    get_user_orders,
    update_order_status,
    cancel_order
)
from app.core.security import get_current_active_user
from app.models.user import User
from app.utils.email.services import send_invoice_email

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order_route(
    order: OrderBase,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_order = create_order(db=db, user_id=current_user.id, order=order)
    
    # Add background task to send invoice
    background_tasks.add_task(
        send_invoice_email,
        user_email=current_user.email,
        order=db_order
    )
    
    return db_order

@router.get("/", response_model=List[OrderOut])
def read_user_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_orders = get_user_orders(db, user_id=current_user.id)
    if not db_orders:
        raise HTTPException(status_code=404, detail="Orders not found")
    return db_orders

@router.get("/{order_id}", response_model=OrderOut)
def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_order = get_order(db, order_id=order_id)
    if not db_order or db_order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.put("/{order_id}/status", response_model=OrderOut)
def update_order_status_route(
    order_id: int,
    status_update: OrderStatusUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_order = update_order_status(db, order_id=order_id, status=status_update.status)
    if not db_order or db_order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if not db_order.status in ["processing"]:
        background_tasks.add_task(
        send_invoice_email,
        user_email=current_user.email,
        order=db_order
    )
        
    return db_order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_order_route(
    order_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_order = cancel_order(db, order_id=order_id, user_id=current_user.id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    background_tasks.add_task(
        send_invoice_email,
        user_email=current_user.email,
        order=db_order
    )
    return {"message": "Order cancelled"}