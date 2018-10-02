from rest_framework import serializers, status
from .models import Profile
from authors.apps.authentications.models import User
from rest_framework.response import response

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer to map the UserProfile instance into JSON format
    """
    username = serializers.CharField(max_length=255, source='user.username')
    bio = serializers.CharField(max_length=255, default='Update your bio')
    image_url = serializers.CharField(max_length=255, default='image-link')
    following = serializers.BooleanField(default=False)

    class Meta:
        model = Profile
        fields = ('username', 'bio', 'image_url', 'following')
        read_only_fields = ['username']