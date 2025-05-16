from app.schemas.user_schema import UserOut
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    product_id: int
    rating: float = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=1, le=5)
    comment: Optional[str] = None

class Review(ReviewBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ReviewOut(BaseModel):
    id: int
    user: Optional[UserOut]
    product_id: int
    rating: float
    comment: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True