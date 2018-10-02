from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import *
from .models import User
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, EmailSerializer, PasswordResetSerializer
)

from django.template.loader import render_to_string


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class EmailSentAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = EmailSerializer

    def post(self, request):
        email = request.data.get('email', {})
        user = User.objects.filter(email=email).first()
        if user is None:
            message = {"message":"The Email provided is not registered"}
            return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = self.serializer_class(data={"email":email})
        serializer.is_valid(raise_exception=True)
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        message = {"message":"We've sent a password reset link to your email"}
        subject = "Password reset"
        body = render_to_string('password_reset.html', {
            'link': 'https://google.com?token=' + token,
            'name': user.username,
        })


        send_mail(subject, "Password Reset", "noreply@Authors-Haven.com", [email], html_message=body)
        return Response(message, status=status.HTTP_200_OK)

class PasswordResetAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = PasswordResetSerializer

    def put(self, request):
        password = request.data.get('password', {})
        email = request.data.get('email', {})
        user = User.objects.filter(email=email).first()
        token = request.GET.get("token", "")
        token_generator = PasswordResetTokenGenerator()
        checked_token = token_generator.check_token(user, token)
        if not checked_token:
           return Response({"message":"invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()  
        data={
            "email":email, 
            "password":password
            }    
        serializer = self.serializer_class(user, data=data)
        serializer.is_valid(raise_exception=True)
        return Response({"message":"password successfully changed"}, status=status.HTTP_202_ACCEPTED)
