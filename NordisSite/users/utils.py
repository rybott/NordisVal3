import qrcode
import base64
from io import BytesIO
import pyotp  # Install with `pip install pyotp`

def generate_mfa_secret():
    """
    Generates a 32-character base32 secret for MFA.
    """
    return pyotp.random_base32()

def generate_mfa_qr(secret_key, user_email):
    """
    Generate a QR Code for MFA setup.
    """
    otp_auth_url = f"otpauth://totp/MyDjangoApp:{user_email}?secret={secret_key}&issuer=MyDjangoApp"

    qr = qrcode.make(otp_auth_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{qr_base64}"
