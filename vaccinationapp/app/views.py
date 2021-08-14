from rest_framework import generics, status
from .serializers import RegisterSerializer, LoginSerializer, CountySerializer, CitySerializer, VaccineSerializer, CategorySerializer, OfficeSerializer, PersonSerializer, AppointmentSerializer, WaitingSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserActivationToken, County, City, Vaccine, Categories, Office, Person, Appointment, Waiting
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
import jwt, datetime
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import calendar

class RegisterView(generics.GenericAPIView):
  # permission_classes = (IsAuthenticated,)

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
  
    # Util.send_email(data)
    return Response(user_data, status=status.HTTP_201_CREATED)



class Verify(generics.GenericAPIView):
  serializer_class = UserActivationToken

  def get(self,request,token):
    try:
      userToken = UserActivationToken.objects.get(token=token)
      user = userToken.getUser()
      userDb = User.objects.get(id = user)
      if not userDb.is_active:
        userDb.is_active = True
        userDb.save()
        userToken.delete()
      return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
    except jwt.ExpiredSignatureError as identifier:
      return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.DecodeError as identifier:
      return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
  


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

class CountyCityDetails(APIView):
  def get(self,request,city):
    counties  = County.objects.all().filter(city=city)
    serializer = CountySerializer(counties, many=True)
    return Response(serializer.data,  status=status.HTTP_200_OK)


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
  def get_object(self, county):
    try:
      return City.objects.all().filter(county=county)
    except City.DoesNotExist:
       return Response(status=status.HTTP_404_NOT_FOUND)

  def get(self, request, county):
    city = self.get_object(county)
    serializer = CitySerializer(city, many=True)
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


class OfficeAppointmentDateDetails(APIView):
  def get(self, request, pk,date):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    office = Office.objects.get(pk=pk)
    
    serializer = OfficeSerializer(office)
  
    hlmit = serializer.data['hourlyLimit'] 

    enddate = datetime.datetime(date.year,12,31)
    delta = enddate - date
    dates=[]
    
    for i in range(delta.days+1):
        x = date + datetime.timedelta(days=i)
        if Appointment.objects.all().filter(office=pk,date=x.strftime("%Y-%m-%d")).count() <  (hlmit*10):
          dates.append(x.strftime("%Y-%m-%d"))
    return Response({"AvailableDates":dates}, status=status.HTTP_200_OK)

class OfficeAppointmentHourDetails(APIView):
  def get(self, request, pk,date):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    office = Office.objects.get(pk=pk)
    serializer = OfficeSerializer(office)
    hlmit = serializer.data['hourlyLimit'] 
    serializer = OfficeSerializer(office)
    hours =[]
    rapelHours=[]
    startingHour= 8
    LastHour = 18
    for i in range(startingHour,LastHour+1):
      if Appointment.objects.all().filter(office=pk,date=date.strftime("%Y-%m-%d"),time=i).count() <  hlmit:
        hours.append(i)

    rapelDay = (date+datetime.timedelta(serializer.data['vaccine']['booster_days'])).strftime("%Y-%m-%d")
    for i in range(startingHour,LastHour+1):
      if Appointment.objects.all().filter(office=pk,date=rapelDay,time=i).count() <  hlmit:
        rapelHours.append(i)

    return Response({"AvailableHours":hours,"RapelDay":rapelDay,"RapelHours":rapelHours}, status=status.HTTP_200_OK)



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

class PersonUserDetails(APIView):
    def get(self,request,user):
      person = Person.objects.all().filter(user=user)
      serializer = PersonSerializer(person, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)



class AppointmentList(APIView):
  def get(self,request):
    appointment = Appointment.objects.all()
    serializer = AppointmentSerializer(appointment, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self,request):
    serializer = AppointmentSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetails(APIView):
  def get_object(self, pk):
    try:
      return Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
       return Response(status=status.HTTP_404_NOT_FOUND)

  def get(self, request, pk):
    appointment = self.get_object(pk)
    serializer = AppointmentSerializer(appointment)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def put(self, request, pk):
    appointment = self.get_object(pk)
    serializer = AppointmentSerializer(appointment, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    appointment = self.get_object(pk)
    appointment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  
class AppointmentUserDetails(APIView):
  def get(self,request,user):
    appointment = Appointment.objects.all().filter(user=user)
    serializer = AppointmentSerializer(appointment, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


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

class UserDetails(APIView):
    def get(self,request,email):
      try:
        user = User.objects.get(email=email)
      except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
      serializer = UserSerializer(user,data={"id":user.id})
      if serializer.is_valid():
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    