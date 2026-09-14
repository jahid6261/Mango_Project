
import smtplib

from email.mime.text import MIMEText
from src.utils.settings import settings


EMAIL_HOST = settings.EMAIL_HOST
EMAIL_PORT = settings.EMAIL_PORT
EMAIL_USER = settings.EMAIL_USER
EMAIL_PASSWORD = settings.EMAIL_PASSWORD
EMAIL_FROM = settings.EMAIL_FROM


def email_utility(email_to: str, email_subject: str, email_body: str):
    msg = MIMEText(email_body)
    msg["Subject"] = email_subject
    msg["From"] = EMAIL_FROM
    msg["To"] = email_to

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)

        return {"success": True, "message": f"Email sent to {email_to}"}

    except Exception as e:
        return {"success": False, "error": str(e)}

def send_activation_email(
    to_email: str,
    first_name: str,
    activation_token: str,
):

    activation_url = (
        f"{settings.BASE_URL}/api/v1/users/activate/{activation_token}"
    )

    email_body = f"""
Hello {first_name},

Welcome to Mango Selling Team.

Your account has been created successfully.

Please click the link below to activate your account:

{activation_url}

After activating your account, you will be able to login.

If you did not create this account, please ignore this email.

Best regards,
Mango Selling Owner
"""

    return email_utility(
        email_to=to_email,
        email_subject="Activate your Mango Selling Team Account",
        email_body=email_body,
    )




def send_password_reset_otp_email(
    to_email: str,
    first_name: str,
    otp: str
):
    email_body = f"""
Hello {first_name},

We received a request to reset the password for your Mango Selling account.

Your password reset OTP is:

{otp}

This OTP will expire in 5 minutes.

If you did not request a password reset, you can safely ignore this email.

Best regards,
Mango Selling Team
"""

    return email_utility(
        email_to=to_email,
        email_subject="Mango Selling - Password Reset OTP",
        email_body=email_body,
    ) 



def send_order_confirmation_email(
    to_email: str,
    first_name: str,
    order_id: int,
    product_total: float,
    delivery_charge: float,
    final_price: float,
):
    email_body = f"""
Hello {first_name},

Thank you for your order from Mango Selling!

Your order has been placed successfully.

Order ID: #{order_id}
Payment Method: Cash on Delivery
Order Status: Pending

Product Total: {product_total} BDT
Delivery Charge: {delivery_charge} BDT
Final Price: {final_price} BDT

You will pay the final price when your order is delivered.

Best regards,
Mango Selling Team
"""

    return email_utility(
        email_to=to_email,
        email_subject=f"Order Confirmation - Order #{order_id}",
        email_body=email_body,
    )




def send_order_completed_email(
    to_email: str,
    first_name: str,
    order_id: int,
    product_total: float,
    delivery_charge: float,
    final_price: float,
):
    email_body = f"""
Hello {first_name},

Your Mango Selling order has been completed successfully.

Order ID: #{order_id}

Payment Method: Cash on Delivery
Order Status: Completed

Product Total: {product_total} BDT
Delivery Charge: {delivery_charge} BDT
Final Price: {final_price} BDT

Thank you for shopping with Mango Selling!

Best regards,
Mango Selling Team
"""

    return email_utility(
        email_to=to_email,
        email_subject=f"Order Completed - Order #{order_id}",
        email_body=email_body,
    )