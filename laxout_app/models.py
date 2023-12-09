from django.db import models
from django.contrib.auth.models import AbstractUser
import random, string
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from datetime import datetime
from django.utils import timezone

def random_string(length=100):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

class Laxout_Exercise(models.Model):
    execution = models.CharField(max_length=400,default="")
    name = models.CharField(max_length=40,default="")
    dauer = models.IntegerField(default=30)
    videoPath = models.CharField(max_length=100,default="")
    looping = models.BooleanField(default=False)
    added = models.BooleanField(default=False)
    instruction = models.CharField(max_length=200, default="")
    timer = models.BooleanField(default=False)
    required = models.CharField(max_length=50, default="")
    imagePath = models.CharField(max_length=50, default="")
    
class Physio(AbstractUser, PermissionsMixin):
    user_uid = models.CharField(max_length=180, default=random_string(), unique=True)
    physio_field1 = models.CharField(max_length=100, default="")
    physio_field2 = models.IntegerField(default=0)


class LaxoutUser(models.Model):
    laxout_user_name = models.CharField(max_length=200, default="")
    laxout_credits = models.IntegerField(default=0)
    note = models.CharField(max_length=200, default="")
    creation_date = models.DateField(default= timezone.now())
    exercises = models.ManyToManyField(Laxout_Exercise)
    created_by = models.ForeignKey(Physio, on_delete=models.CASCADE)