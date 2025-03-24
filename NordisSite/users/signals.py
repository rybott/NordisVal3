from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    """
    Automatically create default roles when running migrations.
    """
    if sender.name == "users":  # Only apply to the users app
        roles = {
            "Admin": ["add_user", "change_user", "delete_user", "view_user"],
            "Analyst": ["add_document", "change_document", "view_document"],
            "Client": ["view_document"]
        }

        for role, perms in roles.items():
            group, created = Group.objects.get_or_create(name=role)
            for perm in perms:
                permission = Permission.objects.filter(codename=perm).first()
                if permission:
                    group.permissions.add(permission)
