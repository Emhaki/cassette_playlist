from django.db import models
import uuid

def generate_short_uuid():
    return str(uuid.uuid4())[:6]

class PlyUser(models.Model):
    uuid = models.CharField(max_length=6, default=generate_short_uuid, editable=False, unique=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    nickname = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    profile_image_url = models.URLField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname