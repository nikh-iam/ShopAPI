from app.models.product import Product
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from typing import List, Optional, Dict

from app.models.category import Category
from app.schemas.category_schema import CategoryCreate, CategoryUpdate

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_by_name(db: Session, name: str) -> Optional[Category]:
    return db.query(Category).filter(Category.name == name).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Dict]:
    results = (
        db.query(
            Category.id,
            Category.name,
            func.count(Product.id).label("product_count")
        )
        .outerjoin(Product, Product.category_id == Category.id)
        .group_by(Category.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        {"id": cat_id, "name": name, "product_count": count}
        for cat_id, name, count in results
    ]

def create_category(db: Session, category: CategoryCreate) -> Category:
    existing = get_category_by_name(db, name=category.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists"
        )
    
    new_category = Category(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def update_category(db: Session, category_id: int, category: CategoryUpdate) -> Optional[Category]:
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        return None
    
    update_data = category.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int) -> bool:
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        return False
    
    db.delete(db_category)
    db.commit()
    return True