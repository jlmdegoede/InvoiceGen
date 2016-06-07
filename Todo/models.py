from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TodoAuth(models.Model):
    auth_token = models.CharField(max_length=200)
    user_id = models.ForeignKey(to=User)
    valid = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)