from rest_framework import serializers
from .models import User, UserActivationToken, County, City
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



class UserActivationTokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = UserActivationToken
        fields = [
            'datetime',
            'user',
            'token'
        ]
    
    def create(self, validated_data):
        return UserActivationToken.objects.create_token(**validated_data)



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,min_length=3)
    password = serializers.CharField(max_length=69,min_length=6,write_only=True)
    tokens = serializers.CharField(max_length=600,read_only=True)

    class Meta:
        model = User
        fields = [
            'email', 
            'password', 
            'tokens'
        ]

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled')
        
        return{
            'email': user.email,
            'tokens': user.tokens
        }

        return super().validate(attrs)



class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = [
            'id', 
            'name',
            'county'
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