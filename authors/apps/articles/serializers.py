from rest_framework import serializers
from .models import ArticlesModel
from authors.apps.authentication.serializers import UserSerializer
from authors.apps.articles.helpers import get_time_to_read_article


class ArticlesSerializers(serializers.ModelSerializer):

    title = serializers.CharField(
        required=True,
        max_length=128,
        error_messages={
            'required': 'Title is required',
            'max_length': 'Title cannot be more than 128'
        }
    )
    description = serializers.CharField(
        required=False,
        max_length=250,
        error_messages={
            'max_length': 'Description should not be more than 250'
        }
    )
    body = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Body is required'
        }
    )

    image_url = serializers.URLField(
        required=False
    )

    author = UserSerializer(
        read_only=True
    )

    def to_representation(self,instance):
       """
       overide representatiom for custom output
       """
       representation = super(ArticlesSerializers, self).to_representation(instance)
       representation['time_to_read'] = get_time_to_read_article(instance)
       return representation
    
    class Meta:
        model = ArticlesModel
        fields = (
            'title',
            'description',
            'body',
            'slug',
            'image_url',
            'author',
            'created_at',
            'updated_at'
        )

