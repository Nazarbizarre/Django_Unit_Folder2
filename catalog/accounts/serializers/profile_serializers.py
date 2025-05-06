from django.contrib.auth.models import User
from rest_framework import serializers
 
from ..models import Profile
from .user_serializers import UserSerializer
 
 
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
 
    class Meta:
        model = Profile
        fields = "__all__"