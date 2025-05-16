from fastapi import Request
from app.models.product import Product
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
from app.core.security import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.utils.email import send_invoice_email

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order_route(
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
async def read_user_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_orders = get_user_orders(db, user_id=current_user.id)
    if not db_orders:
        raise HTTPException(status_code=404, detail="Orders not found")
    return db_orders

@router.get("/{order_id}", response_model=OrderOut)
async def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_order = get_order(db, order_id=order_id)
    if not db_order or db_order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.put("/{order_id}", response_model=OrderOut)
async def update_order_status_route(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    db_order = get_order(db, order_id=order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    db_order = update_order_status(db, order_id=order_id, status=status_update.status)

    return db_order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_order_route(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_order = get_order(db, order_id)
    if not db_order or (not current_user.is_admin and db_order.user_id != current_user.id):
        raise HTTPException(status_code=404, detail="Order not found")

    if db_order.status not in ["placed", "processing"]:
        raise HTTPException(
            status_code=400,
            detail="Order cannot be cancelled as it's already shipped or delivered"
        )

    for item in db_order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock += item.quantity

    db_order.status = "cancelled"
    db.commit()

    return {"message": "Order cancelled"}
