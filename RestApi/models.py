from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class SessionIDs(models.Model):
    device_token = models.CharField(max_length=700)
    user = models.ForeignKey(User)
    session_id = models.CharField(max_length=200)
    date_created = models.DateField()
    valid = models.BooleanField()
    device = models.CharField(max_length=100)
    software_version = models.CharField(max_length=10)
    last_known_ip = models.CharField(max_length=100)

    def serialize(self):
        return {"session_id": self.session_id, "username": self.user.username}