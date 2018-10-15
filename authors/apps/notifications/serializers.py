# authors/apps/notifications/serializers.py

from rest_framework import serializers
from django.utils.timesince import timesince

from authors.apps.articles.models import ArticlesModel
from authors.apps.articles.serializers import ArticlesSerializers
from authors.apps.authentication.models import User
from authors.apps.notifications.models import UserNotifications 

from rest_framework import serializers
from django.utils.timesince import timesince


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        """
        Notification fields to be returned to users
        """
        model = UserNotifications
        fields = ('read_status', 'created_at', 'notification', 'article')
