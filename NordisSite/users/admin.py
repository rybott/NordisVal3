from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "is_staff", "is_active")

    # Convert fieldsets to a mutable list
    fieldsets = list(UserAdmin.fieldsets)

    # Ensure "groups" is added ONLY if it is NOT already present
    existing_fields = [field for section in fieldsets for field in section[1].get("fields", [])]

    if "groups" not in existing_fields:
        fieldsets.append(("Roles", {"fields": ("groups",)}))

    # Convert back to tuple (Django expects tuples)
    fieldsets = tuple(fieldsets)

admin.site.register(CustomUser, CustomUserAdmin)
