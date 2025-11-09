from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class UserSeralizers(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True , required = True )
    class Meta:
        model = User
        fields = ['id','username','email','password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])

        return super().create(validated_data)    