from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from laxout_app import models 



@api_view(['POST'])
def autorise_laxout_user(request):
    user_uid = request.data['user_uid']
    
    try:
        user = models.LaxoutUser.objects.get(user_uid=user_uid)
    except models.LaxoutUser.DoesNotExist:
        return Response({'details': 'user not found'})
    
    physio_instance = user.created_by
    
    if not isinstance(physio_instance, models.Physio):
        return Response({'details': 'physio not found for the given user'})
    
    token, created = Token.objects.get_or_create(user=physio_instance)
    
    return Response({"token": token.key})