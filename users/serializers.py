from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import User
from rest_framework.authtoken.models import Token

class SignUpSerializer(serializers.ModelSerializer):
    # email = serializers.CharField(max_length = 80)
    first_name = serializers.CharField(max_length = 45)
    last_name = serializers.CharField(max_length = 45)
    username = serializers.CharField(max_length = 45)
    password = serializers.CharField(min_length = 6, write_only=True)
    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'password')
    def validate(self, attrs):
        username_exist = User.objects.filter(username=attrs['username']).exists()

        if username_exist:
            raise serializers.ValidationError({
                "username": "This username has already been used."
            })

        return super().validate(attrs)
    
    def create(self,validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user = user)
        return user