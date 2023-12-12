from django.db import models
from django.contrib.auth.models import User
import random, string
from django.contrib.auth.models import AbstractUser,PermissionsMixin, User
from datetime import datetime
from django.utils import timezone
from uuid import uuid4

def random_string(length=70):
    allowed_characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(allowed_characters) for _ in range(length))
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
    appId = models.IntegerField(default=0)
    
# class Physio(AbstractUser, PermissionsMixin):
#     user_uid = models.CharField(max_length=180, default=random_string(), unique=True)
#     physio_field1 = models.CharField(max_length=100, default="")
#     physio_field2 = models.IntegerField(default=0)

class LaxoutUser(models.Model):
    user_uid = models.CharField(max_length=420, default=str(uuid4()), unique=True)
    laxout_user_name = models.CharField(max_length=200, default="")
    laxout_credits = models.IntegerField(default=0)
    note = models.CharField(max_length=200, default="")
    creation_date = models.DateField(default= timezone.now())
    exercises = models.ManyToManyField(Laxout_Exercise)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    