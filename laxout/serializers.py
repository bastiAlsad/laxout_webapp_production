from rest_framework import serializers
from laxout_app import models


class LaxoutUSerSerializer(serializers.ModelSerializer):
        class Meta(object):
             model = models.LaxoutUser
             fields = ['__all__']