def base_email_template(content: str) -> str:
    return f"""
    <html>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 20px; display: flex; justify-content: center; color: #333;">
        <div style="width: 100%; max-width: 800px; background-color: #f5f5f5; margin: auto;">
            {content}
                <!-- Footer section -->
                <div style="border-top: 1px solid #eee; margin: 30px 0;"></div>
                
                <div style="text-align: center; font-size: 14px;">
                    <p style="margin: 5px 0;">If you have any questions, feel free to contact our customer support.</p>
                    <p style="margin: 5px 0; font-weight: bold;">- The Epic Games Team</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

def build_order_content(order) -> str:
    items_html = ""
    for item in order.items:
        items_html += f"""
        <tr style="border-bottom: 1px solid #ddd;">
            <td style="padding: 15px; text-align: left; font-size: 14px;">{item.product.title}</td>
            <td style="padding: 15px; text-align: left; font-size: 14px;">{item.quantity}</td>
            <td style="padding: 15px; text-align: right; font-size: 14px; font-weight: normal;">₹{item.price:.2f} INR</td>
        </tr>
        """

    # discounts_html = ""
    # if order.discount_amount > 0:
    #     discounts_html = f"""
    #     <tr style="background-color: #f7f7f7;">
    #         <td colspan="2" style="padding: 15px; text-align: left; font-size: 14px;">Discounts:</td>
    #             <td style="padding: 15px; text-align: right; font-size: 14px;"></td>
    #     </tr>
    #     <tr>
    #         <td colspan="2" style="padding: 15px; text-align: left; font-size: 14px;">Sale Discount</td>
    #             <td style="padding: 15px; text-align: right; font-size: 14px;">- ₹539.00 INR</td>
    #     </tr>
    #     """

    return f"""
            <div style="background-color: #fff; border-radius: 5px; padding: 40px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <!-- Greeting section -->
                <div style="text-align: center; margin-bottom: 30px;">
                    <h2 style="font-size: 24px; margin-bottom: 5px;">Hi {order.user.first_name}!</h2>
                    <p style="font-size: 16px; margin: 5px 0;">Thank you for your purchase!</p>
                </div>
                
                <!-- Invoice ID section -->
                <div style="text-align: center; margin-bottom: 40px;">
                    <h1 style="font-size: 24px; font-weight: bold; margin-bottom: 5px; color: #333;">INVOICE ID:</h1>
                    <h2 style="font-size: 28px; font-weight: bold; margin-top: 5px;">{order.id}</h2>
                </div>
                
                <!-- Order information section -->
                <div style="margin-bottom: 30px;">
                    <h3 style="color: #999; font-size: 14px; text-transform: uppercase; margin-bottom: 15px; font-weight: 600; letter-spacing: 0.5px;">YOUR ORDER INFORMATION:</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div style="margin-bottom: 10px;">
                            <p style="margin: 5px 0; font-size: 14px;"><strong style="font-weight: 600;">Order ID:</strong></p>
                            <p style="margin: 5px 0; font-size: 14px;">{order.id}</p>
                        </div>
                        <div style="margin-bottom: 10px;">
                            <p style="margin: 5px 0; font-size: 14px;"><strong style="font-weight: 600;">Bill To:</strong></p>
                            <p style="margin: 5px 0; font-size: 14px;"><a href="mailto:{order.user.email}" style="color: #0078f2; text-decoration: none;">mathewnikhil432@gmail.com</a></p>
                        </div>
                        <div style="margin-bottom: 10px;">
                            <p style="margin: 5px 0; font-size: 14px;"><strong style="font-weight: 600;">Order Date:</strong></p>
                            <p style="margin: 5px 0; font-size: 14px;">{order.order_date.strftime('%B %d, %Y')}</p>
                        </div>
                        <div style="margin-bottom: 10px;">
                            <p style="margin: 5px 0; font-size: 14px;"><strong style="font-weight: 600;">Source:</strong></p>
                            <p style="margin: 5px 0; font-size: 14px;">ShopAPI Store</p>
                        </div>
                    </div>
                </div>
                
                <!-- Order details table -->
                <div>
                    <h3 style="color: #999; font-size: 14px; text-transform: uppercase; margin-bottom: 15px; font-weight: 600; letter-spacing: 0.5px;">HERE'S WHAT YOU ORDERED:</h3>
                    <table style="width: 100%; border-collapse: collapse; margin-bottom: 30px;">
                        <thead style="background-color: #f7f7f7;">
                            <tr>
                                <th style="padding: 15px; text-align: left; font-size: 14px;">Description:</th>
                                <th style="padding: 15px; text-align: left; font-size: 14px;">Quantity:</th>
                                <th style="padding: 15px; text-align: right; font-size: 14px;">Price:</th>
                            </tr>
                        </thead>
                        <tbody>
                            {items_html}
                            <tr style="font-weight: bold; border-top: 1px solid #ddd;">
                                <td colspan="2" style="padding: 15px; text-align: left; font-size: 14px;">TOTAL:</td>
                                <td style="padding: 15px; text-align: right; font-size: 14px;">₹{order.total_amount:.2f} INR</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
    """

def build_welcome_content(first_name: str) -> str:
    return f"""
        <h2 style="color:#4CAF50; text-align: center;">Welcome to ShopAPI!</h2>
        <p style="text-align: center;">Hi {first_name}, we're excited to have you on board.</p>

        <div style="margin-top: 30px;">
            <p><strong>OTP:</strong> </p>
        </div>
        <hr style="margin: 20px 0; border: none; border-top: 1px solid #eee;" />

        <p style="text-align: center;">Start shopping and discover great products today.</p>
        <p style="text-align: center;">If you have any questions, we're always here to help.</p>
    """
