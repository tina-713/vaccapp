from rest_framework import serializers
from .models import User, UserActivationToken, County, City, Vaccine, Categories, Office, Person, Appointment, Waiting
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=69, min_length=6, write_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'email', 
            'password'
        ]

    def validate(self, attrs):
        email = attrs.get('email', '')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



# class UserActivationTokenSerializer(serializers.ModelSerializer):
#     token = serializers.CharField(max_length=555,read_only=True)

#     class Meta:
#         model = UserActivationToken
#         fields = [
#             'datetime',
#             'user',
#             'token'
#         ]
    
#     def create(self, validated_data):
#         return UserActivationToken.objects.create_token(**validated_data)



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,min_length=3)
    password = serializers.CharField(max_length=69,min_length=6,write_only=True)
    refresh = serializers.CharField(max_length=600,read_only=True)
    access = serializers.CharField(max_length=600,read_only=True)

    class Meta:
        model = User
        fields = [
            'email', 
            'password', 
            'refresh',
            'access'
        ]

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        user.SetTokens()
        print(user)
        if not user:
            raise AuthenticationFailed('Invalid credentials')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled')
        
        return{
            'email': user.email,
            'refresh': user.refresh,
            'access': user.access
        }




class OfficeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Office
        fields = [
            'id',
            'city',
            'name', 
            'addres',
            'phone',
            'spots',
            'vaccine'
        ]



class CitySerializer(serializers.ModelSerializer):
    office = OfficeSerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = [
            'id', 
            'name',
            'county',
            'office'
        ]



class CountySerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = County
        fields = [
            'id', 
            'name',
            'cities'
        ]



class VaccineSerializer(serializers.ModelSerializer):
    office = OfficeSerializer(many=True, read_only=True)

    class Meta:
        model = Vaccine
        fields = [
            'id', 
            'name',
            'booster_days',
            'office'
        ]



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = [
            'id',
            'risk_count', 
            'name',
            'description'
        ]



class PersonSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(write_only=True)
    # city = serializers.CharField(write_only=True)
    # category = serializers.CharField(write_only=True)

    class Meta:
        model = Person
        fields = [
            'user',
            'id',
            'name', 
            'last_name',
            'cnp',
            'gender',
            'age',
            'phone',
            'email',
            'city',
            'category'
        ]



class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = [
            'person',
            'status',
            'office',
            'kind', 
            'date'
        ]



class WaitingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Waiting
        fields = [
            'person',
            'office',
            'spot'
        ]

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 
        ]