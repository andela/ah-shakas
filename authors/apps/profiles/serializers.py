from rest_framework import serializers, status
from .models import Profile
from authors.apps.authentication.models import User
from rest_framework.response import Response

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer to map the UserProfile instance into JSON format
    """
    username = serializers.CharField(max_length=255, source='user.username')
    bio = serializers.CharField(max_length=255, default='Update your bio')
    image_url = serializers.CharField(max_length=255, default='image-link')
    following = serializers.BooleanField(default=False)


    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        super(ProfileSerializer, self).update(instance, validated_data)
        if user_data is not None and user_data.get('username') is not None:
            instance.user.username = user_data.get('username')
            instance.user.save()
        return instance

    class Meta:
        model = Profile
        fields = ('username', 'bio', 'image_url', 'following')
        read_only_fields = ['username']