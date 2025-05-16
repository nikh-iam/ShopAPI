# tests/test_services.py
import pytest
from sqlalchemy.orm import Session
from app.services import (
    user_service,
    product_service,
    category_service,
    cart_service,
    order_service,
    review_service
)

from app.schemas.user_schema import UserCreate, UserUpdate
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.schemas.cart_schema import CartItemCreate
from app.schemas.order_schema import OrderBase
from app.schemas.review_schema import ReviewCreate, ReviewUpdate

from app.models import User, Product, Category
from app.models.order import Order, OrderItem
from app.models.cart import Cart, CartItem
from app.models.review import Review

def test_user_services(db_session: Session):
    # Test create_user
    user_data = UserCreate(
        email="service@test.com",
        password="password",
        first_name="Service",
        last_name="Test"
    )
    user = user_service.create_user(db_session, user_data)
    assert user.email == "service@test.com"
    
    # Test get_user_by_email
    found_user = user_service.get_user_by_email(db_session, "service@test.com")
    assert found_user.id == user.id
    
    # Test authenticate_user
    auth_user = user_service.authenticate_user(db_session, "service@test.com", "password")
    assert auth_user is not None
    
    # Test update_user
    update_data = UserUpdate(first_name="Updated")
    updated_user = user_service.update_user(db_session, user.id, update_data, user)
    assert updated_user.first_name == "Updated"
    
    # Test delete_user
    assert user_service.delete_user(db_session, user.id, user) is True

def test_product_services(db_session: Session, test_category: Category):
    # Test create_product
    product_data = ProductCreate(
        title="Service Product",
        description="Test Description",
        price=9.99,
        category_id=test_category.id,
        stock=50
    )
    product = product_service.create_product(db_session, product_data)
    assert product.title == "Service Product"
    
    # Test get_product
    found_product = product_service.get_product(db_session, product.id)
    assert found_product.id == product.id
    
    # Test update_product
    update_data = ProductUpdate(price=12.99)
    updated_product = product_service.update_product(db_session, product.id, update_data)
    assert updated_product.price == 12.99
    
    # Test delete_product
    assert product_service.delete_product(db_session, product.id) is True

def test_category_services(db_session: Session):
    # Test create_category
    category_data = CategoryCreate(name="Service Category")
    category = category_service.create_category(db_session, category_data)
    assert category.name == "Service Category"
    
    # Test get_category
    found_category = category_service.get_category(db_session, category.id)
    assert found_category.id == category.id
    
    # Test update_category
    update_data = CategoryUpdate(name="Updated Category")
    updated_category = category_service.update_category(db_session, category.id, update_data)
    assert updated_category.name == "Updated Category"
    
    # Test delete_category
    assert category_service.delete_category(db_session, category.id) is True

def test_cart_services(db_session: Session, test_user: User, test_product: Product):
    # Test add_to_cart
    cart_item_data = CartItemCreate(product_id=test_product.id, quantity=2)
    cart = cart_service.add_to_cart(db_session, test_user.id, cart_item_data)
    assert cart is not None
    assert len(cart["items"]) == 1
    assert cart["items"][0]["product_id"] == test_product.id
    assert cart["items"][0]["quantity"] == 2
    
    # Test update_cart_item
    cart_item_id = cart["items"][0]["id"]
    updated_cart = cart_service.update_cart_item(db_session, test_user.id, cart_item_id, 3)
    assert updated_cart is not None
    assert updated_cart["items"][0]["quantity"] == 3
    
    # Test remove_from_cart
    updated_cart = cart_service.remove_from_cart(db_session, test_user.id, cart_item_id)
    assert updated_cart is not None
    assert len(updated_cart["items"]) == 0
    
    # Test clear_cart
    assert cart_service.clear_cart(db_session, test_user.id) is True
    
    # Verify cart is empty
    empty_cart = cart_service.get_user_cart(db_session, test_user.id)
    assert empty_cart is None or len(empty_cart["items"]) == 0

def test_order_services(db_session: Session, test_user: User, test_product: Product):
    # Create a cart with items first
    cart_item_data = CartItemCreate(product_id=test_product.id, quantity=2)
    cart_service.add_to_cart(db_session, test_user.id, cart_item_data)
    
    # Test create_order
    order_data = OrderBase(
        shipping_address="123 Test St",
        payment_method="credit_card"
    )
    order = order_service.create_order(db_session, test_user.id, order_data)
    assert order.total_amount == test_product.price * 2
    
    # Test get_order
    found_order = order_service.get_order(db_session, order.id)
    assert found_order.id == order.id
    
    # Test update_order_status
    updated_order = order_service.update_order_status(db_session, order.id, "processing")
    assert updated_order.status == "processing"
    
    # Test cancel_order
    cancel_order = order_service.cancel_order(db_session, order.id, test_user.id)
    assert cancel_order.status == "cancelled"

def test_review_services(db_session: Session, test_user: User, test_product: Product, test_order: Order):
    # Test create_review
    review_data = ReviewCreate(
        product_id=test_product.id,
        rating=5,
        comment="Great product"
    )
    review = review_service.create_review(db_session, review_data, test_user.id)
    assert review.rating == 5
    
    # Test get_reviews_by_product
    reviews = review_service.get_reviews_by_product(db_session, test_product.id)
    assert len(reviews) == 1
    
    # Test update_review
    update_data = ReviewUpdate(rating=4)
    updated_review = review_service.update_review(db_session, review.id, test_user.id, update_data)
    assert updated_review.rating == 4
    
    # Test delete_review
    assert review_service.delete_review(db_session, review.id, test_user.id) is True