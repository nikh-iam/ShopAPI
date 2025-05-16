from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.orm import aliased
from fastapi import HTTPException
from typing import List, Optional

from app.models.product import Product
from app.models.category import Category
from app.models.review import Review
from app.schemas.product_schema import ProductCreate, ProductUpdate

def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    return db.query(Product).offset(skip).limit(limit).all()

def get_products_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 100) -> List[Product]:
    return db.query(Product).filter(Product.category_id == category_id).offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate) -> Product:
    db_category = db.query(Category).filter(Category.id == product.category_id).first()
    if not db_category:
        raise HTTPException(status_code=400, detail="Category not found")
    
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: ProductUpdate) -> Optional[Product]:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return None
    
    if product.category_id:
        db_category = db.query(Category).filter(Category.id == product.category_id).first()
        if not db_category:
            raise HTTPException(status_code=400, detail="Category not found")
    
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int) -> bool:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return False
    
    db.delete(db_product)
    db.commit()
    return True

def search_products(
    db: Session,
    query: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None,
    category_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Product]:
    avg_rating_subquery = (
        db.query(
            Review.product_id,
            func.avg(Review.rating).label("avg_rating")
        )
        .group_by(Review.product_id)
        .subquery()
    )

    ProductAlias = aliased(Product)

    q = db.query(Product).outerjoin(
        avg_rating_subquery, Product.id == avg_rating_subquery.c.product_id
    )

    if query:
        q = q.filter(Product.title.ilike(f"%{query}%"))

    if min_price is not None:
        q = q.filter(Product.price >= min_price)
    if max_price is not None:
        q = q.filter(Product.price <= max_price)
    if category_id is not None:
        q = q.filter(Product.category_id == category_id)
    if min_rating is not None:
        q = q.filter(avg_rating_subquery.c.avg_rating >= min_rating)

    return q.offset(skip).limit(limit).all()

def calculate_avg_product_ratings(db: Session, product_id: int):
    rating_sum = 0
    ratings = db.query(Review).filter(Review.product_id == product_id).order_by(Review.created_at.desc()).all()
    for rating in ratings:
        rating_sum += rating.rating

    avg_rating = rating_sum / len(ratings)
    return avg_rating, len(ratings)