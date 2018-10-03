from rest_framework import serializers
from .models import ArticlesModel

<<<<<<< HEAD

class ArticlesSerializers(serializers.ModelSerializer):

=======
class ArticlesSerializers(serializers.ModelSerializer):
    # author = serializers.CharField(source='author.username')
>>>>>>> [Feature #160577480] Initial Commit
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

    class Meta:
        model = ArticlesModel
        fields = (
            'title',
            'description',
            'body',
            'slug',
            'author',
            'createdAt',
            'updatedAt')
