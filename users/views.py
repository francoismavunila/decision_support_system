from rest_framework.authtoken.models import Token
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
            user_data = serializer.save()
            token, created = Token.objects.get_or_create(user=user_data)
            user = serializer.data
            response = {
                "message": "User created successfully",
                "data":user,
                "token": token.key
            }
            return Response(data = response, status=status.HTTP_201_CREATED)
        errors = serializer.errors
        formatted_errors = {"message": " ".join([f"{field}: {str(err[0])}" for field, err in errors.items()])}
        return Response(data=formatted_errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            serializer = self.serializer_class(user)
            response = {
                "message": "User logged in successfully",
                "data": serializer.data,
                "token": token.key
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {
                "message": "Invalid username or password",
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)