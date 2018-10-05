from rest_framework import status, generics
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .models import User
from .renderers import UserJSONRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, EmailSerializer, PasswordResetSerializer
)
from .password_token import generate_password_token, get_password_token_data
import os
from django.template.loader import render_to_string


class RegistrationAPIView(CreateAPIView):
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


class LoginAPIView(CreateAPIView):
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

class EmailSentAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = EmailSerializer

    def post(self, request):
        """
        here, the user provides email to be used to get a link. The email must be registered,
        token gets generated and sent to users via link.
        """
        email = request.data.get('email', {})
        serializer = self.serializer_class(data={"email":email})
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            message = {"message":"The email provided is not registered"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        token_generator = PasswordResetTokenGenerator()
        password_token = token_generator.make_token(user)
        token = generate_password_token(email, password_token)
        message = {"message":"We've sent a password reset link to your email"}
        subject = "Password reset"
        reset_link = os.getenv('PASSWORD_RESET')
        body = render_to_string('password_reset.html', {
            'link':reset_link+'?token=' + token,
            'name': user.username,
        })
        sender = os.getenv('EMAIL_SENDER')
        send_mail(subject, "Password Reset", sender, [email], html_message=body)
        return Response(message, status=status.HTTP_200_OK)

class PasswordResetAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = PasswordResetSerializer

    def put(self, request):
        """
        Here, the user has received an email with a link to reset password.
        The user provides a new password.
        Token gets verified against the user.
        Once all checks have passed, the new password gets saved.
        """
        user_token = request.GET.get("token", "")
        try:
            token_data = get_password_token_data(user_token)
            if not token_data['email']:
                return Response({"message":"invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except :
            return Response({"message":"invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        password = request.data.get('password', {})
        email = token_data['email']
        data={
            "email":email,
            "password":password
            }
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            message = {"message":"The Email provided is not registered"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        token = token_data['token']
        token_generator = PasswordResetTokenGenerator()
        checked_token = token_generator.check_token(user, token)
        if not checked_token:
           return Response({"message":"invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(user, data=data)
        serializer.is_valid(raise_exception=True)
        user.set_password(password)
        user.save()
        serializer = self.serializer_class(user, data=data)
        serializer.is_valid(raise_exception=True)
        return Response({"message":"password successfully changed"}, status=status.HTTP_200_OK)
