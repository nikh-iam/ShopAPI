import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings
from app.models.order import Order

def send_invoice_email(user_email: str, order: Order):
    # SMTP server configuration
    SMTP_SERVER = settings.SMTP_SERVER
    SMTP_PORT = settings.SMTP_PORT
    SMTP_USERNAME = settings.SMTP_USERNAME
    SMTP_PASSWORD = settings.SMTP_PASSWORD
    FROM_EMAIL = SMTP_USERNAME

    # Create the email subject
    subject = f"Your ShopAPI order #{order.id}"

    # Create the HTML body
    items_html = ""
    for item in order.items:
        items_html += f"""
        <tr>
            <td style="padding: 8px;">{item.product.title}</td>
            <td style="padding: 8px; text-align: center;">{item.quantity}</td>
            <td style="padding: 8px; text-align: right;">${item.price:.2f}</td>
        </tr>
        """

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px; color: #333;">

        <h2 style="color: #4CAF50;">{order.status.capitalize()}</h2>
        <p>Hello {order.user.first_name},</p>

        <p>Here is the summary of your order:</p>

        <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
            <tr>
                <td><strong>Order ID:</strong></td>
                <td>#{order.id}</td>
            </tr>
            <tr>
                <td><strong>Total Amount:</strong></td>
                <td>${order.total_amount:.2f}</td>
            </tr>
            <tr>
                <td><strong>Shipping Address:</strong></td>
                <td>{order.shipping_address}</td>
            </tr>
            <tr>
                <td><strong>Payment Method:</strong></td>
                <td>{order.payment_method}</td>
            </tr>
        </table>

        <h3>Order Items:</h3>
        <table style="width: 100%; border: 1px solid #eee; border-collapse: collapse;">
            <thead style="background-color: #f9f9f9;">
                <tr>
                    <th style="padding: 10px; text-align: left;">Product</th>
                    <th style="padding: 10px; text-align: center;">Quantity</th>
                    <th style="padding: 10px; text-align: right;">Price</th>
                </tr>
            </thead>
            <tbody>
                {items_html}
            </tbody>
        </table>

        <p style="margin-top: 30px;">Thank you for choosing ShopAPI!</p>

        <p>Best Regards,<br><strong>ShopAPI Team</strong></p>
    </body>
    </html>
    """

    # Create MIME message
    message = MIMEMultipart("alternative")
    message["From"] = FROM_EMAIL
    message["To"] = user_email
    message["Subject"] = subject

    # Attach HTML body
    message.attach(MIMEText(html_body, "html"))

    # Send the email
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(message)
            print(f"Invoice email sent to {user_email}")
    except Exception as e:
        print(f"Failed to send invoice email: {e}")
