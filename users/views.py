from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import parser_classes,api_view
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSeralizers
# Create your views here.


@api_view(['GET','POST'])

def user_list_create(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return Response({'detail':'Authentication credentials were not provided'},status=401)
        users = User.objects.all()
        serializer = UserSeralizers(users,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserSeralizers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
