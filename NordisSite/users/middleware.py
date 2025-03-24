from django.shortcuts import redirect
from django.urls import reverse

class EnforceMfaMiddleware:
    """
    Middleware to enforce MFA after login if enabled.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Check if user has MFA enabled and hasn't completed MFA yet
            if request.user.mfa_enabled and not request.session.get("mfa_authenticated"):
                if request.path not in [reverse("verify_mfa"), reverse("logout")]:
                    return redirect("verify_mfa")  # Force MFA verification

        return self.get_response(request)
