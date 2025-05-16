# tests/conftest.py
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem
from app.models.review import Review
from app.core.security import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()  # Rollback any uncommitted transactions
        db.close()
        # Clear all data but keep tables
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(db_session):
    email = f"test_{datetime.now().timestamp()}@example.com"
    user = User(
        email=email,
        hashed_password=get_password_hash("testpassword"),
        first_name="Test",
        last_name="User",
        is_active=True,
        is_admin=False
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture(scope="function")
def test_admin(db_session):
    email = f"admin_{datetime.now().timestamp()}@example.com"
    admin = User(
        email=email,
        hashed_password=get_password_hash("adminpassword"),
        first_name="Admin",
        last_name="User",
        is_active=True,
        is_admin=True
    )
    db_session.add(admin)
    db_session.commit()
    return admin

@pytest.fixture(scope="function")
def test_category(db_session):
    name = f"Test Category {datetime.now().timestamp()}"
    category = Category(name=name)
    db_session.add(category)
    db_session.commit()
    return category

@pytest.fixture(scope="function")
def test_product(db_session, test_category):
    product = Product(
        title=f"Test Product {datetime.now().timestamp()}",
        description="Test Description",
        price=10.99,
        category_id=test_category.id,
        stock=100
    )
    db_session.add(product)
    db_session.commit()
    return product

@pytest.fixture(scope="function")
def test_cart(db_session, test_user):
    cart = Cart(user_id=test_user.id)
    db_session.add(cart)
    db_session.commit()
    return cart

@pytest.fixture(scope="function")
def test_cart_item(db_session, test_cart, test_product):
    cart_item = CartItem(
        cart_id=test_cart.id,
        product_id=test_product.id,
        quantity=2
    )
    db_session.add(cart_item)
    db_session.commit()
    return cart_item

@pytest.fixture(scope="function")
def test_order(db_session, test_user, test_product):
    order = Order(
        user_id=test_user.id,
        shipping_address="123 Test St",
        payment_method="credit_card",
        total_amount=test_product.price * 2,
        status="placed"
    )
    db_session.add(order)
    db_session.commit()
    
    order_item = OrderItem(
        order_id=order.id,
        product_id=test_product.id,
        quantity=2,
        price=test_product.price
    )
    db_session.add(order_item)
    db_session.commit()
    return order

@pytest.fixture(scope="function")
def test_review(db_session, test_user, test_product, test_order):
    review = Review(
        user_id=test_user.id,
        product_id=test_product.id,
        rating=5,
        comment="Great product!"
    )
    db_session.add(review)
    db_session.commit()
    return review

@pytest.fixture(scope="function")
def user_token(client, test_user):
    response = client.post(
        "/users/login",
        data={"username": test_user.email, "password": "testpassword"}
    )
    return response.json()["access_token"]

@pytest.fixture(scope="function")
def admin_token(client, test_admin):
    response = client.post(
        "/users/login",
        data={"username": test_admin.email, "password": "adminpassword"}
    )
    return response.json()["access_token"]