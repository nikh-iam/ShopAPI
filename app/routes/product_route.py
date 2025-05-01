from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.product_schema import (
    ProductCreate, 
    ProductOut, 
    ProductUpdate,
    ProductList
)
from app.services.product_service import (
    get_product,
    get_products,
    create_product,
    update_product,
    delete_product,
    search_products,
    get_products_by_category
)
from app.core.security import get_current_active_user, get_current_admin_user
from app.models.user import User

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductOut])
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    products = get_products(db, skip=skip, limit=limit)
    return products

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product_route(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return create_product(db=db, product=product)

@router.get("/{product_id}", response_model=ProductOut)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=ProductOut)
def update_product_route(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    db_product = update_product(db=db, product_id=product_id, product=product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_route(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    delete_product(db=db, product_id=product_id)
    return

@router.get("/search/", response_model=List[ProductOut])
def search_products_route(
    query: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    return search_products(db=db, query=query)