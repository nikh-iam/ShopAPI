from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.schemas.review_schema import ReviewOut

class ProductBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    stock: int = Field(0, ge=0)
    images: Optional[List[str]] = None
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    images: Optional[List[str]] = None
    category_id: Optional[int] = None

class ProductOut(ProductBase):
    id: int
    reviews: Optional[List[ReviewOut]] = []
    average_rating: Optional[float] = 0.0
    review_count: Optional[int] = 0
    
    class Config:
        orm_mode = True

class ProductList(BaseModel):
    products: List[ProductOut]