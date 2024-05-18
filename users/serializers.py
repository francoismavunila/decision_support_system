# users/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=15)

    def validate(self, data):
        if not data.get('username'):
            raise serializers.ValidationError('Username is required')
        if not data.get('phone_number'):
            raise serializers.ValidationError('Phone number is required')
        return data
    
    
    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            phone_number=validated_data['phone_number'],
        )
        return user
