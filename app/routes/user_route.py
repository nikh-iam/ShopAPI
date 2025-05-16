# app/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.order_schema import OrderOut
from app.schemas.review_schema import ReviewOut
from app.schemas.user_schema import (
    UserCreate, UserOut, UserUpdate, Token
)
from app.services.user_service import (
    create_user, authenticate_user, get_orders, get_user_by_id,
    get_user_orders, get_user_reviews, get_users, update_user, delete_user
)
from app.core.security import (
    create_access_token, get_current_active_user, get_current_admin_user
)
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.put("/me", response_model=UserOut)
def update_user_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return update_user(db=db, user_id=current_user.id, user_update=user_update, current_user=current_user)

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    delete_user(db=db, user_id=current_user.id, current_user=current_user)
    return

# Admin-only per-user routes
@router.get("/users", response_model=List[UserOut])
def admin_read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return get_users(db, skip=skip, limit=limit)

@router.get("/orders", response_model=List[OrderOut])
def admin_read_all_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return get_orders(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserOut)
def admin_read_user_by_id(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return get_user_by_id(db=db, user_id=user_id)

@router.put("/{user_id}", response_model=UserOut)
def admin_update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return update_user(db=db, user_id=user_id, user_update=user_update, current_user=current_user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    delete_user(db=db, user_id=user_id, current_user=current_user)
    return

@router.get("/{user_id}/orders", response_model=List[OrderOut])
def admin_get_user_orders(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return get_user_orders(db, user_id, skip=skip, limit=limit)

@router.get("/{user_id}/reviews", response_model=List[ReviewOut])
def admin_get_user_reviews(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return get_user_reviews(db, user_id, skip=skip, limit=limit)
