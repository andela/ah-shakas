#  authors/apps/notifications
# Contains the views for the notifications

import jwt
from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
from rest_framework.renderers import JSONRenderer
from authors.apps.notifications.models import UserNotifications
from authors.apps.authentication.models import User
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

from authors.apps.authentication.serializers import (UserSerializer)


class NotificationAPIView(generics.ListAPIView):
    """
    A View that returns notifications
    """
    renderer_classes = (JSONRenderer, )
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        notifications = UserNotifications.objects.all()
        content = {'Notifications': notifications}
        return Response(content)


class SubscribeAPIView(generics.ListAPIView):
    """
    A view for subcribing for notifications
    """

    renderer_classes = (JSONRenderer, )
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    def get(self, request):
        email = request.user
        user = User.objects.get(email=email)
        if user.is_subcribed == True:
            return Response({"Message":"You are already subscribed to notifications"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.is_subcribed = True
            user.save()
            return Response({"Message":"You have successfully subscribed to notifications"}, status=status.HTTP_200_OK)
            serializer = self.serializer_class(request.user)
            return Response(serializer.data)

class UnSubscribeAPIView(generics.ListAPIView):
    """
    A view for Unsubcribing for notifications
    """

    renderer_classes = (JSONRenderer, )
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    def get(self, request):
        email = request.user
        user = User.objects.get(email=email)
        if user.is_subcribed == False:
            return Response({"Message": "You are not subscribed to notifications"})
        else:
            user.is_subcribed = False
            user.save()
            return Response({"Message": "You have successfully unsubscribed to notifications"})
            serializer = self.serializer_class(request.user)
            return Response(serializer.data)