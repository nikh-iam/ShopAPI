from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional

from app.models.product import Product
from app.models.category import Category
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
    
    db_product = Product(**product.dict())
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
    
    update_data = product.dict(exclude_unset=True)
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

def search_products(db: Session, query: str) -> List[Product]:
    return db.query(Product).filter(Product.title.ilike(f"%{query}%")).all()