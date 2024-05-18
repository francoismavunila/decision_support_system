# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from .models import User as UserModel

class User(APIView):
    def post(self, request):
        # get password and pop it out
        password = request.data.pop('password', None)
        serializer = UserSerializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = UserModel.objects.get(username = request.data['username'])
            user.set_password(password)
            user.save()
            return Response({'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request):
        user = UserModel.objects.get(username = "jk")
        serializer = UserSerializer(user, many=False)
        return Response({'users': serializer.data})