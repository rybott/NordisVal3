from django.contrib.auth import get_user_model
from django.core.signing import Signer
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from users.utils import generate_mfa_qr, generate_mfa_secret
import pyotp  # Install with `pip install pyotp`
from django.contrib import messages
from django.views import View

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

User = get_user_model()
signer = Signer()

def invite_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        user = User.objects.create(email=email, username=email, is_activated=False)
        token = signer.sign(email)
        activation_link = request.build_absolute_uri(reverse("activate_user", args=[token]))

        send_mail(
            "Activate Your Account",
            f"Click here to activate: {activation_link}",
            "admin@yourdomain.com",
            [email],
        )
        return render(request, "base/base.html")  # A simple confirmation page

    return render(request, "invite_user.html")


def activate_user(request, token):
    try:
        email = signer.unsign(token)
        user = User.objects.get(email=email)
        user.is_activated = True
        user.save()

        # Redirect user directly to password reset request with email prefilled
        reset_url = reverse("password_reset") + f"?email={email}"
        return redirect(reset_url)

    except Exception:
        return render(request, "activation_failed.html")

class CustomLoginView(LoginView):
    """
    Custom Login View to enforce MFA only if the user has set it up.
    """
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        # Skip MFA for admin users (superusers)
        if user.is_superuser:
            return redirect("admin:index")  # Redirect to Django Admin

        # Only redirect to MFA if MFA is enabled AND the user has an MFA secret key
        if user.mfa_enabled and user.mfa_secret:
            return redirect("verify_mfa")

        return redirect('webinterface:hom')  # If no MFA, go directly to dashboard

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('webinterface:hom')




@login_required
def enable_mfa(request):
    user = request.user

    # Generate a secret key if the user doesn't already have one
    if not user.mfa_secret:
        user.mfa_secret = generate_mfa_secret()
        user.save()

    # Generate QR Code
    qr_code = generate_mfa_qr(user.mfa_secret, user.email)

    if request.method == "POST":
        mfa_code = request.POST.get("mfa_code")
        totp = pyotp.TOTP(user.mfa_secret)
        if totp.verify(mfa_code):
            user.mfa_enabled = True
            user.save()
            messages.success(request, "MFA enabled successfully!")
            return redirect("sites")
        else:
            messages.error(request, "Invalid MFA code. Try again.")

    return render(request, "enable_mfa.html", {"qr_code": qr_code})


@login_required
def verify_mfa(request):
    user = request.user

    if not user.mfa_enabled:
        return redirect("site")  # Skip MFA if not enabled

    if request.method == "POST":
        mfa_code = request.POST.get("mfa_code")
        totp = pyotp.TOTP(user.mfa_secret)
        if totp.verify(mfa_code):
            request.session["mfa_authenticated"] = True  # Mark MFA as passed
            return redirect("sites")
        else:
            messages.error(request, "Invalid MFA code. Try again.")

    return render(request, "verify_mfa.html")


@login_required
def disable_mfa(request):
    user = request.user

    if request.method == "POST":
        password = request.POST.get("password")
        if authenticate(username=user.username, password=password):
            user.mfa_enabled = False
            user.mfa_secret = None
            user.save()
            messages.success(request, "MFA disabled successfully!")
            return redirect("sites")
        else:
            messages.error(request, "Incorrect password. Try again.")

    return render(request, "disable_mfa.html")
