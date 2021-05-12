from django.shortcuts import render
from rest_framework import generics, status, viewsets
from .serializers import RegisterSerializer, UserActivationTokenSerializer, LoginSerializer, CountySerializer, CitySerializer, VaccineSerializer, CategorySerializer, OfficeSerializer, PersonSerializer, AppointmentSerializer, WaitingSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserActivationToken, County, City, Vaccine, Categories, Office, Person, Appointment, Waiting
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import get_object_or_404
import datetime
from rest_framework.views import APIView


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



class Login(generics.GenericAPIView):
  serializer_class = LoginSerializer

  def post(self,request):
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)

    return Response(serializer.data, status=status.HTTP_200_OK)



class CountyList(APIView):
  def get(self,request):
    counties  = County.objects.all()
    serializer = CountySerializer(counties, many=True)
    return Response(serializer.data,  status=status.HTTP_200_OK)
  
  def post(self,request):
    serializer = CountySerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CountyDetails(APIView):
  def get_object(self, pk):
    try:
      return County.objects.get(pk=pk)
    except County.DoesNotExist:
       return Response(status=status.HTTP_404_NOT_FOUND)

  def get(self, request, pk):
    county = self.get_object(pk)
    serializer = CountySerializer(county)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def put(self, request, pk):
    county = self.get_object(pk)
    serializer = CountySerializer(county, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    county = self.get_object(pk)
    county.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



class CityList(APIView):
  def get(self,request):
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self,request):
    serializer = CitySerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CityDetails(APIView):
  def get_object(self, pk):
    try:
      return City.objects.get(pk=pk)
    except City.DoesNotExist:
       return Response(status=status.HTTP_404_NOT_FOUND)

  def get(self, request, pk):
    city = self.get_object(pk)
    serializer = CitySerializer(city)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def put(self, request, pk):
    city = self.get_object(pk)
    serializer = CitySerializer(city, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    city = self.get_object(pk)
    city.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



class VaccineList(APIView):
  def get(self, request):
    if request.method == 'GET':
      vaccine = Vaccine.objects.all()
      serializer = VaccineSerializer(vaccine, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)



class CategoryList(APIView):
  
  def get(self,request):
    category = Categories.objects.all()
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



class OfficeList(APIView):
  def get(self,request):
    office = Office.objects.all()
    serializer = OfficeSerializer(office, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self,request):
    serializer = OfficeSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OfficeDetails(APIView):
  def get_object(self, pk):
    try:
      return Office.objects.get(pk=pk)
    except Office.DoesNotExist:
       return Response(status=status.HTTP_404_NOT_FOUND)

  def get(self, request, pk):
    office = self.get_object(pk)
    serializer = OfficeSerializer(office)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def put(self, request, pk):
    office = self.get_object(pk)
    serializer = OfficeSerializer(office, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    office = self.get_object(pk)
    office.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



class PersonList(APIView):
  def get(self,request):
    person = Person.objects.all()
    serializer = PersonSerializer(person, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self,request):
    serializer = PersonSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonDetails(APIView):
  def get_object(self, pk):
    try:
      return Person.objects.get(pk=pk)
    except Person.DoesNotExist:
       return Response(status=status.HTTP_404_NOT_FOUND)

  def get(self, request, pk):
    person = self.get_object(pk)
    serializer = PersonSerializer(person)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def put(self, request, pk):
    person = self.get_object(pk)
    serializer = PersonSerializer(person, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    person = self.get_object(pk)
    person.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



class AppointmentList(APIView):
  def get(self,request):
    appointment = Appointment.objects.all()
    serializer = AppointmentSerializer(appointment, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self,request):
    serializer = AppointmentSerializer(data=request.data, many=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class WaitingList(APIView):
  def get(self,request):
    waiting = Waiting.objects.all()
    serializer = WaitingSerializer(waiting, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self,request):
    serializer = WaitingSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WaitingDetails(APIView):
  def get_object(self, pk):
    try:
      return Waiting.objects.get(pk=pk)
    except Waiting.DoesNotExist:
       return Response(status=status.HTTP_404_NOT_FOUND)

  def get(self, request, pk):
    waiting = self.get_object(pk)
    serializer = WaitingSerializer(waiting)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def put(self, request, pk):
    waiting = self.get_object(pk)
    serializer = WaitingSerializer(waiting, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    waiting = self.get_object(pk)
    waiting.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)