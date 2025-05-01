from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.category_schema import (
    CategoryCreate, 
    CategoryOut, 
    CategoryUpdate,
    CategoryWithProducts
)
from app.services.category_service import (
    get_category,
    get_categories,
    create_category,
    update_category,
    delete_category
)
from app.core.security import get_current_active_user, get_current_admin_user
from app.models.user import User

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[CategoryOut])
def read_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_categories(db, skip=skip, limit=limit)

@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category_route(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return create_category(db=db, category=category)

@router.get("/{category_id}", response_model=CategoryWithProducts)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = get_category(db, category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.put("/{category_id}", response_model=CategoryOut)
def update_category_route(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    db_category = update_category(db=db, category_id=category_id, category=category)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category_route(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    delete_category(db=db, category_id=category_id)
    return