import re
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # To hide password while GET

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username', 'password', 'phone_number']



class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username', 'password', 'phone_number']


    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(' Eamil already exists')
        return value
    
    def validate_phone_number(self, value):
        # Accepts patterns like +1234567890 or 1234567890
        pattern = re.compile(r'^\+?\d{5,15}$')
        if value and not pattern.match(value):
            raise serializers.ValidationError("Invalid phone number format.")
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data) # automatically hash password and save user details.
        return user


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            
            if not user:
                raise serializers.ValidationError('Invalid user credentials !')
            data['user'] = user # Storing email, password, user object 
            
        else:
            raise serializers.ValidationError('Must include Email and Password')
        
        return data