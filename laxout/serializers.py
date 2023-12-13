from rest_framework import serializers
from laxout_app import models


class LaxoutUSerSerializer(serializers.ModelSerializer):
        class Meta(object):
             model = models.LaxoutUser
             fields = ['__all__']


class LaxoutExerciseSerializer(serializers.ModelSerializer):
       class Meta(object):
              model = models.Laxout_Exercise
              fields = ["id","execution", "name", "dauer", "videoPath", "looping", "added", "instruction", "timer", "required", "imagePath", "appId"]
              encoding = 'utf-8'

class CouponSerializer(serializers.ModelSerializer):
       class Meta(object):
              fiels = ["id", "coupon_name", "coupon_text", " coupon_image_url", "coupon_price", "coupon_offer", "rabbat_code"]