from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RegisterSerializer, UserActivationTokenSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserActivationToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import get_object_or_404
import datetime


class RegisterView(generics.GenericAPIView):
  serializer_class = RegisterSerializer

  def post(self, request):
    user = request.data
    serializer = self.serializer_class(data=user)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user_data = serializer.data
    user = User.objects.get(email=user_data['email'])
    
    token = RefreshToken.for_user(user).access_token
    current_site = get_current_site(request).domain

    #absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
    #email_body = ' Use the link below to verify your email \n' + absurl
    #data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}

    now = datetime.datetime.now()
    UserToken = UserActivationToken()
   
    UserToken.create_token(token=token,datetime=now,user=user_data['id'])
   
    absurl = 'http://'+current_site+"/auth/verify/"+str(UserToken)
    email_body = ' Use the link below to verify your email \n' + absurl
    data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}
  
    Util.send_email(data)
    return Response(user_data, status=status.HTTP_201_CREATED)


class Verify(generics.GenericAPIView):
  serializer_class = UserActivationToken

  def get(self,request,token):
    userToken = UserActivationToken.objects.get(token=token)
    user = userToken.getUser()
    userDb = User.objects.get(id = user)
    userDb.is_active = True
    userDb.save()
    userToken.delete()
    return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
