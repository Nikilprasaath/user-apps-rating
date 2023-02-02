from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from .models import app, user_profile, tasks

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        # print(validated_data['username'])
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.groups.add(2)
        user_profile.objects.create(user=user)
        user.set_password(validated_data['password'])
        user.save()
        
        return user

class AdminRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        # print(validated_data['username'])
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.groups.add(1)
        user.set_password(validated_data['password'])
        user.save()
        
        return user


class nameserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name']

class appserializer(serializers.ModelSerializer):
    class Meta:
        model = app
        fields = '__all__'

class user_profile_serializer(serializers.ModelSerializer):
    apps = appserializer(many=True)
    user = nameserializer()
    class Meta:
        model = user_profile
        fields = '__all__'


class taskserializer(serializers.ModelSerializer):
    # user = nameserializer()
    class Meta:
        model = tasks
        fields = '__all__'


class admintaskserializer(serializers.ModelSerializer):
    
    class Meta:
        model = tasks
        fields = '__all__'
 