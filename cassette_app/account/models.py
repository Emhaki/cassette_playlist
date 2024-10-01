from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class PlyUser(models.Model):
    id = models.CharField(primary_key=True, auto_created=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    nickname = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname