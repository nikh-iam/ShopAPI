from pydantic import BaseModel, Field
from typing import List
from app.schemas.product_schema import ProductOut

class CartItemBase(BaseModel):
    product_id: int
    quantity: int = Field(1, gt=0)

class CartItemCreate(CartItemBase):
    pass

class CartItemOut(CartItemBase):
    id: int
    product: dict
    
    class Config:
        orm_mode = True

class CartOut(BaseModel):
    id: int
    user_id: int
    items: List[CartItemOut] = []
    total_items: int = 0
    total_price: float = 0.0
    
    class Config:
        orm_mode = True