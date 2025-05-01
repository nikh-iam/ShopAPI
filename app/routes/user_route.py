from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.utils.email.services import send_welcome_email
from app.schemas.user_schema import (
    UserCreate, 
    UserOut, 
    UserUpdate, 
    Token
)
from app.services.user_service import (
    get_user_by_email,
    create_user,
    authenticate_user,
    get_users,
    update_user,
    delete_user
)
from app.core.security import (
    create_access_token,
    get_current_active_user,
    get_current_admin_user
)
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    created_user = create_user(db=db, user=user)
    background_tasks.add_task(
        send_welcome_email,
        user_email=created_user.email,
        user_name=created_user.first_name
    )
    return created_user

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
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
    return update_user(
        db=db,
        user_id=current_user.id,
        user_update=user_update,
        current_user=current_user
    )

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    delete_user(db=db, user_id=current_user.id, current_user=current_user)
    return

# Admin-only endpoints
@router.get("/", response_model=List[UserOut])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return get_users(db, skip=skip, limit=limit)

@router.put("/{user_id}", response_model=UserOut)
def update_user_admin(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return update_user(
        db=db,
        user_id=user_id,
        user_update=user_update,
        current_user=current_user
    )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    delete_user(db=db, user_id=user_id, current_user=current_user)
    return

# @router.get("/addresses", response_model=List[AddressBase])
# def get_user_addresses_route(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_active_user)
# ):
#     return user_service.get_user_addresses(db, user_id=current_user.id)

# @router.get("/addresses/{address_id}", response_model=AddressBase)
# def get_user_address_route(
#     address_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_active_user)
# ):
#     address = user_service.get_address_by_id(db, address_id, user_id=current_user.id)
#     if not address:
#         raise HTTPException(status_code=404, detail="Address not found")
#     return address

# @router.post("/addresses", response_model=AddressBase)
# def create_address_route(
#     address_create: AddressCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_active_user)
# ):
#     return user_service.create_address(db, user_id=current_user.id, address_create=address_create)

# @router.put("/addresses/{address_id}", response_model=AddressBase)
# def update_address_route(
#     address_id: int,
#     address_update: AddressUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_active_user)
# ):
#     return user_service.update_address(db, address_id, user_id=current_user.id, address_update=address_update)

# @router.delete("/addresses/{address_id}", status_code=204)
# def delete_address_route(
#     address_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_active_user)
# ):
#     if not user_service.delete_address(db, address_id, user_id=current_user.id):
#         raise HTTPException(status_code=404, detail="Address not found")
#     return
