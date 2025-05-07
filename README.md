# 🛍️ ShopAPI

A complete E-Commerce backend built with **FastAPI**, supporting user authentication, product management, shopping cart, orders, and more — with **role-based access control** for users and admins.

---

## Features

- **User Management**
- **Product & Category CRUD**
- **Shopping Cart**
- **Orders**
- **JWT Authentication with Role-based Access**
- **Admin Controls**

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nikh-iam/ShopAPI.git
cd ShopAPI
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate     
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` File

```env
# APPLICATION
PROJECT_NAME=ShopAPI
VERSION=1.0.0

# DATABASE
DATABASE_URL=sqlite:///shop_app.db

# JWT
SECRET_KEY=shop_app_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ADMIN CREDENTIALS
DEFAULT_ADMIN_EMAIL=admin@gmail.com
DEFAULT_ADMIN_PASSWORD=12345678

# EMAIL (Optional for future use)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USERNAME=your_email_id
SMTP_PASSWORD=your_email_app_passcode
```

---

## Run the Application

```bash
uvicorn app:app --reload
```

Visit: **http://localhost:8000**

- Swagger: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

---

## Authentication

ShopAPI uses OAuth2 + JWT token-based authentication.

- **Login**: `/users/login`
- **Secure Endpoints** require:

```
Authorization: Bearer <token>
```

---

## API Endpoints

### 👤 User Management

| Endpoint                | Method | Description                     | Auth Required | Request Body                              | Response (Success)         |
|------------------------|--------|---------------------------------|---------------|-------------------------------------------|----------------------------|
| `/users/register`      | POST   | Register new user               | No            | `UserCreate`                              | `201`: `UserOut`           |
| `/users/login`         | POST   | Login user                      | No            | `username`, `password`                    | `200`: `Token`             |
| `/users/me`            | GET    | Get current user profile        | Yes           | -                                         | `200`: `UserOut`           |
| `/users/me`            | PUT    | Update current user profile     | Yes           | `UserUpdate`                              | `200`: `UserOut`           |
| `/users/me`            | DELETE | Delete current user             | Yes           | -                                         | `204`: No Content          |
| `/users/`              | GET    | List all users (Admin only)     | Yes (Admin)   | -                                         | `200`: `[UserOut]`         |
| `/users/{user_id}`     | PUT    | Update user (Admin)             | Yes (Admin)   | `UserUpdate`                              | `200`: `UserOut`           |
| `/users/{user_id}`     | DELETE | Delete user (Admin)             | Yes (Admin)   | -                                         | `204`: No Content          |

---

### 📦 Product Management

| Endpoint                  | Method | Description               | Auth Required | Request Body      | Response               |
|---------------------------|--------|---------------------------|---------------|-------------------|------------------------|
| `/products/`              | POST   | Create product (Admin)    | Yes (Admin)   | `ProductCreate`   | `201`: `ProductOut`    |
| `/products/{id}`          | GET    | Get product by ID         | No            | -                 | `200`: `ProductOut`    |
| `/products/{id}`          | PUT    | Update product (Admin)    | Yes (Admin)   | `ProductUpdate`   | `200`: `ProductOut`    |
| `/products/{id}`          | DELETE | Delete product (Admin)    | Yes (Admin)   | -                 | `204`: No Content      |
| `/products/search/`       | GET    | Search products by query  | No            | `query` param     | `200`: `[ProductOut]`  |

---

### 🗂️ Category Management

| Endpoint                        | Method | Description                 | Auth Required | Request Body       | Response                     |
|---------------------------------|--------|-----------------------------|---------------|--------------------|------------------------------|
| `/categories/`                 | GET    | List all categories         | No            | -                  | `200`: `[CategoryOut]`       |
| `/categories/`                 | POST   | Create category (Admin)     | Yes (Admin)   | `CategoryCreate`   | `201`: `CategoryOut`         |
| `/categories/{id}`            | GET    | Get category and products   | No            | -                  | `200`: `CategoryWithProducts`|
| `/categories/{id}`            | PUT    | Update category (Admin)     | Yes (Admin)   | `CategoryUpdate`   | `200`: `CategoryOut`         |
| `/categories/{id}`            | DELETE | Delete category (Admin)     | Yes (Admin)   | -                  | `204`: No Content            |

---

### 🛒 Shopping Cart

| Endpoint                  | Method | Description                  | Auth Required | Request Body       | Response           |
|---------------------------|--------|------------------------------|---------------|--------------------|--------------------|
| `/cart/`                  | GET    | View current user's cart     | Yes           | -                  | `200`: `CartOut`   |
| `/cart/add`               | POST   | Add item to cart             | Yes           | `CartItemCreate`   | `200`: `CartOut`   |
| `/cart/update/{id}`       | PUT    | Update item quantity         | Yes           | `quantity` param   | `200`: `CartOut`   |
| `/cart/remove/{id}`       | DELETE | Remove item from cart        | Yes           | -                  | `200`: `CartOut`   |
| `/cart/clear`             | DELETE | Clear entire cart            | Yes           | -                  | `204`: No Content  |

---

### 📦 Order Management

| Endpoint                       | Method | Description                  | Auth Required | Request Body        | Response            |
|--------------------------------|--------|------------------------------|---------------|---------------------|---------------------|
| `/orders/`                    | GET    | List all user orders         | Yes           | -                   | `200`: `[OrderOut]` |
| `/orders/`                    | POST   | Create a new order           | Yes           | `OrderBase`         | `201`: `OrderOut`   |
| `/orders/{id}`                | GET    | Get specific order details   | Yes           | -                   | `200`: `OrderOut`   |
| `/orders/{id}`                | DELETE | Cancel order                 | Yes           | -                   | `204`: No Content   |
| `/orders/{id}/status`         | PUT    | Update status (Admin only)   | Yes (Admin)   | `OrderStatusUpdate` | `200`: `OrderOut`   |

---

## Example Request Models

### `UserCreate`
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "strongpassword"
}
```

### `ProductCreate`
```json
{
  "title": "Smart Watch",
  "price": 99.99,
  "category_id": 2
}
```

### `CartItemCreate`
```json
{
  "product_id": 1,
  "quantity": 2
}
```

### `OrderBase`
```json
{
  "shipping_address": "123 Main St, NY",
  "payment_method": "Credit Card",
  "items": [
    { "product_id": 1, "quantity": 2, "price": 10.99 }
  ]
}
```

---

## Default Admin Login
You can set in .env file.
```json
{
  "email": "admin@gmail.com",
  "password": "12345678"
}
```

---

## Future Enhancements

#### API's
- Product Reviews & Ratings  
- Wishlist API  
- Recommendations & Personalization  

#### Frontend
- Home page
- Admin Dashboard

---

## Project Structure

```
ShopAPI/
├── app/
│   ├── main.py
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── core/
│   └── utils/
├── .env
├── requirements.txt
├── README.md
└── run.py
```

---

## License

MIT License. Use freely with attribution.

---

## Contributors

- [Nikhil A Mathew](https://github.com/NikhilAMathew)