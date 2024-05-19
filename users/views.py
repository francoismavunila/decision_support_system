# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from .models import User 
from django.contrib.auth import authenticate

class CreateUser(APIView):
    def post(self, request):
        # get password and pop it out
        password = request.data.pop('password', None)
        serializer = UserSerializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = User.objects.get(username = request.data['username'])
            user.set_password(password)
            user.save()
            return Response({'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username, password)
        user = authenticate(username="admin", password="12345")
        print("the value of status",user)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)