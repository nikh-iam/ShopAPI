from pydantic import BaseModel, Field
from typing import List, Optional

from app.schemas.product_schema import ProductOut

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=50)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)

class CategoryOut(CategoryBase):
    id: int
    
    class Config:
        orm_mode = True

class CategoryWithProducts(CategoryOut):
    products: List['ProductOut'] = []