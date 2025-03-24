from django.urls import path
from django.contrib.auth import views as auth_views
from .views import invite_user, activate_user, enable_mfa, verify_mfa, disable_mfa,CustomLoginView, CustomLogoutView

app_name = 'users'

urlpatterns = [
    path("invite/", invite_user, name="invite_user"),
    path("activate/<str:token>/", activate_user, name="activate_user"),

    # Built-in Django authentication views
    path("login/",  CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("mfa/setup/", enable_mfa, name="enable_mfa"),  # Setup MFA
    path("mfa/verify/", verify_mfa, name="verify_mfa"),  # MFA Verification
    path("mfa/disable/", disable_mfa, name="disable_mfa"),  # Disable MFA
]
