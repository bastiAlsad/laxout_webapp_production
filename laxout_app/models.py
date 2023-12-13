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

def generate_rabatt_code():
    allowed_characters = string.ascii_letters+string.digits
    random_string = ""
    for _ in range(10):
        random_string += random.choice(allowed_characters)
        

class IndexesLaxoutUser(models.Model):
    index = models.IntegerField(default=0)
    creation_date = models.DateField(default=timezone.now())
    created_by = models.IntegerField(default=None, blank=True)

class IndexesPhysios(models.Model):
    index = models.IntegerField(default=0)
    creation_date = models.DateField(default=timezone.now())
    created_by = models.IntegerField(default=None, blank=True)


class Coupon(models.Model):
    coupon_name = models.CharField(default="", max_length=200)
    coupon_text = models.CharField(default="", max_length=400)
    coupon_image_url = models.CharField(default="", max_length=200)
    coupon_price = models.IntegerField(default=0)
    coupon_offer = models.CharField(default="", max_length=100)
    rabbat_code = models.CharField(default="", max_length=250)

class Pains(models.Model):
    paint_amount = models.IntegerField(default=0)



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
    indexes = models.ManyToManyField(IndexesLaxoutUser)
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    indexes = models.ManyToManyField(IndexesPhysios)
    average_pain = models.ManyToManyField(Pains)

    