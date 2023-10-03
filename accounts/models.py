from django.contrib.auth.models import AbstractUser
from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name
    
class  Role(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name
    
class CustomUser(AbstractUser):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        null=True, blank=True
    )