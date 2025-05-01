from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.schemas.product_schema import ProductOut
from app.schemas.user_schema import UserOut

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemOut(OrderItemBase):
    id: int
    product: ProductOut
    
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    shipping_address: str = Field(..., max_length=200)
    payment_method: str = Field(..., max_length=50)
    items: List[OrderItemCreate]

class OrderOut(OrderBase):
    id: int
    user: UserOut
    status: str
    total_amount: float
    order_date: datetime
    items: List[OrderItemOut]
    
    class Config:
        orm_mode = True

class OrderStatusUpdate(BaseModel):
    status: str = Field(..., max_length=20)