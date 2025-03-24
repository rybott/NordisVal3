from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class CustomUser(AbstractUser):
    is_activated = models.BooleanField(default=False)  # Users start as inactive
    created_by_admin = models.BooleanField(default=True)  # Ensures admin-only creation

    # MFA Fields
    mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.email  # Use email instead of username

    def assign_role(self, role_name):
        """
        Assigns a user to a role (group) in Django.
        """
        group, created = Group.objects.get_or_create(name=role_name)
        self.groups.add(group)


class UserInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")

    # Personal Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)  # If not already in CustomUser

    # Company Information
    company_role = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=500)
    company_website = models.URLField(blank=True, null=True)

    # Address (Optional)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company_name}"
