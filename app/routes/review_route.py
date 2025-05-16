from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.review_schema import ReviewCreate, ReviewOut, ReviewUpdate, Review
from app.services.review_service import create_review, get_reviews_by_product, update_review, delete_review
from app.core.security import (
    get_current_active_user,
    get_current_admin_user
)
from app.models.user import User

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=Review, status_code=status.HTTP_201_CREATED)
def add_review(review_in: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return create_review(db, review_in, current_user.id)

@router.get("/product/{product_id}", response_model=List[ReviewOut])
def get_reviews(product_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = get_reviews_by_product(db, product_id, skip=skip, limit=limit)
    if reviews is None:
        HTTPException(
            status_code=404,
            detail="Reviews not found"
        )
    return reviews

@router.put("/{review_id}", response_model=Review)
def edit_review(review_id: int, update_in: ReviewUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    updated_data = update_review(db, review_id, current_user.id, update_in)
    if not updated_data:
        raise HTTPException(status_code=404, detail="Review not found or unauthorized")
    return updated_data

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_review(review_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    success = delete_review(db, review_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Review not found or unauthorized")
    return
