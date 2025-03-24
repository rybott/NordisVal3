from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings

def user_upload_path(instance, filename):
    return f'user_uploads/{instance.user.id}/{filename}'

class UserDocument(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Stores when the file was uploaded
    created_date = models.DateTimeField(auto_now_add=True)  # Stores when the record was created

    def __str__(self):
        return f"{self.user.username} - {self.file.name} (Uploaded: {self.uploaded_at})"
