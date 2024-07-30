from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User


class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username' ,'email' , 'role' , 'password'  , 'first_name' , 'last_name']
        extra_kwargs = {'password': {'write_only': True} }


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','username' , 'password' ]
