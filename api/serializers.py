# api/serializers.py
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","first_name", "last_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}
    
    def validate_email(self, value):
        if User.objects.filter(email= value).exists():
            raise serializers.ValidationError("User already exists")
        return value
    
    def create(self, validated_data):
        # We use create_user to ensure password hashing happens
        user = User.objects.create_user(**validated_data)
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # 1. Get the standard token (which only has user_id)
        token = super().get_token(user)

        # 2. Add custom claims
        token['email'] = user.email
        # You can add more fields here if you want:
        # token['username'] = user.username
        # token['is_admin'] = user.is_superuser

        return token