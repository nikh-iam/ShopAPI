from app.models.product import Product
from app.models.user import User
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models.order import Order, OrderItem
from app.models.review import Review
from app.schemas.review_schema import ReviewCreate, ReviewUpdate
from typing import List, Optional

def create_review(db: Session, review_in: ReviewCreate, user_id: int) -> Optional[Review]:
    existing_review = db.query(Review).filter(
        Review.user_id == user_id,
        Review.product_id == review_in.product_id
    ).first()

    if existing_review:
        raise HTTPException(
            status_code=400, 
            detail="You have already reviewed this product."
        )

    has_bought = db.query(Order).join(OrderItem).filter(
        Order.user_id == user_id,
        OrderItem.product_id == review_in.product_id
    ).first()

    if not has_bought:
        raise HTTPException(
            status_code=403,
            detail="You can only review products you've purchased"
        )

    review = Review(**review_in.model_dump(), user_id=user_id)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_reviews_by_product(db: Session, product_id: int, skip: int = 0, limit: int = 100) -> List[Review]:
    return (
        db.query(Review)
        .options(
            joinedload(Review.product),  
            joinedload(Review.user),   
        )
        .filter(Review.product_id == product_id)
        .order_by(Review.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def update_review(db: Session, review_id: int, user_id: int, update_data: ReviewUpdate) -> Optional[Review]:
    review = db.query(Review).filter(Review.id == review_id, Review.user_id == user_id).first()
    if not review:
        return None
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(review, field, value)
    db.commit()
    db.refresh(review)
    return review

def delete_review(db: Session, review_id: int, user_id: int) -> bool:
    review = db.query(Review).filter(Review.id == review_id, Review.user_id == user_id).first()
    if not review:
        return False
    db.delete(review)
    db.commit()
    return True
