from app.models.order import Order
from app.utils.email.templates import build_order_content, build_welcome_content
from app.utils.email.common import send_email

def send_welcome_email(user_email: str, user_name: str):
    subject = "Welcome to ShopAPI!"
    content = build_welcome_content(user_name)
    send_email(subject, user_email, content)

def send_invoice_email(user_email: str, order: Order):
    subject = f"Your ShopAPI order #{order.id} has been {order.status}"
    content = build_order_content(order)
    send_email(subject, user_email, content)
