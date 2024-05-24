from django.shortcuts import render
from .serializers import SignUpSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
# Create your views here.

class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]
    def post(self, request:Request):
        data = request.data
        
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "User created successfully",
                "date":serializer.data
            }
            return Response(data = response, status=status.HTTP_201_CREATED)
        return Response(data = serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request:Request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        
        if user is not None:
            response = {
                "message": "User logged in successfully",
                "token": user.auth_token.key
            }
            return Response(data= response, status = status.HTTP_200_OK)
        else:
            return Response(data="invalid user name or password",status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request:Request):
        response = {
            "user":str(request.user),
            "auth":str(request.auth)
        }
        
        return Response(data=response, status=status.HTTP_200_OK)