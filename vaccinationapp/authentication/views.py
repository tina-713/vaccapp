from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RegisterSerializer, EmailVerificationSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserActivationToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import get_object_or_404


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
    relativeLink = reverse('email-verify')
    absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
    email_body = ' Use the link below to verify your email \n' + absurl
    data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}

    Util.send_email(data)
    return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
  serializer_class = EmailVerificationSerializer

  def get(request, token):
    user_token = get_object_or_404(UserActivationToken, token=token) 
    if not user_token.user_id == request.user.id:  # check token belongs to the current user 

      time_now = timezone.now()  # current time
    if user_token.datetime > (time_now - timedelta(hours=2)):
      request.user_token.delete()  # delete expired token
    return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
