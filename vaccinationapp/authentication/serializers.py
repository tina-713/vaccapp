from rest_framework import serializers
from .models import User, UserActivationToken


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=69, min_length=6, write_only=True)
    
    class Meta:
        model = User
        fields = ['id','email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class UserActivationTokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = UserActivationToken
        fields = ['datetime','user','token']
    

    def create(self, validated_data):
        return UserActivationToken.objects.create_token(**validated_data)
