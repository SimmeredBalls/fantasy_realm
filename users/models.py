from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gold = models.PositiveIntegerField(default=100) # Every new player gets 100 gold

    def __str__(self):
        return f"Profile for {self.user.username}"