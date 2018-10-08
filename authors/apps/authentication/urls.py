from django.urls import path
from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, EmailSentAPIView, PasswordResetAPIView
)
<<<<<<< HEAD


=======
>>>>>>> 77ecb5063c8a30b5362bd7bc7767bf8bd2f346f7
# Specify a namespace
app_name="authentication"

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view(), name='user-registration'),
    path('users/login/', LoginAPIView.as_view(), name='user_login'),
    path('users/email_sent', EmailSentAPIView.as_view(), name='email_password'),
    path('users/password_reset', PasswordResetAPIView.as_view(), name='password_reset'),
]
