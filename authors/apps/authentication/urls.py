from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, EmailSentAPIView, PasswordResetAPIView
)

# Specify a namespace
app_name="authentication"

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view(), name='user-registration'),
    path('users/login/', LoginAPIView.as_view()),
    path('users/email_sent', EmailSentAPIView.as_view()),
    path('users/password_reset', PasswordResetAPIView.as_view()),
]
