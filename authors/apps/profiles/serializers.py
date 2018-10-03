from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator

from .models import Profile
from authors.apps.authentication.models import User
from rest_framework.response import Response

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer to map the UserProfile instance into JSON format
    """
    username = serializers.RegexField(
        regex='^(?!.*\ )[A-Za-z\d\-\_]+$',
        min_length=4,
        required=True,
        source='user.username',
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Username must be unique',
            )
        ],
        error_messages={
            'invalid': 'Username cannot have a space',
            'required': 'Username is required',
            'min_length': 'Username must have at least 4 characters'
        }
    )
    bio = serializers.CharField(max_length=255, default='Update your bio')
    image_url = serializers.URLField(max_length=250, default='image-link')
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