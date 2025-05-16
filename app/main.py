from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import (
    user_route, 
    product_route, 
    category_route,
    order_route, 
    cart_route,
    review_route
)
from app.core.database import engine, Base, get_db
from app.models import user, product, category, order, cart, review
from app.core.config import settings
from app.utils.create_admin import init_admin_user

def init_db():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    init_admin_user(db)

# Call init_db() once at startup
init_db()

description = """   
ShopAPI is a complete ecommerce web app providing endpoints for:
- User authentication and management
- Product catalog
- Shopping cart functionality
- Order processing
"""

tags_metadata = [
    {
        "name": "users",
        "description": "Manage users. Register, login, update profile, etc."
    },
    {
        "name": "products",
        "description": "Manage products. Admin can create, update, delete products."
    },
    {
        "name": "categories",
        "description": "Manage product categories. Admin can create, update, delete categories."
    },
    {
        "name": "cart",
        "description": "Shopping cart operations. Add/remove items."
    },
    {
        "name": "orders",
        "description": "Manage orders. Only authenticated users can create and track orders."
    },
    {
        "name": "reviews",
        "description": "Manage reviews. Only authenticated users can create, edit and delete reviews."
    }
]

app = FastAPI(
    title=settings.PROJECT_NAME, 
    version=settings.VERSION,
    description=description, 
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0"
    },
    openapi_tags=tags_metadata
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
# Include routers
app.include_router(user_route.router)
app.include_router(product_route.router)
app.include_router(category_route.router)
app.include_router(cart_route.router)
app.include_router(order_route.router)
app.include_router(review_route.router)

@app.get("/", tags=["root"])
async def root():
    return {"message": "ShopAPI is running"}