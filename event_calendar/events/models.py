from tkinter import CASCADE
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (AbstractUser) 

class AppUser(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


#only modification I made was the foreign key tying back to the logged in user that way it only displays their events
class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    starts_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(AppUser, on_delete=CASCADE, related_name='events')

