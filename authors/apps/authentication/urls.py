from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, EmailSentAPIView, PasswordResetAPIView
)
<<<<<<< HEAD

=======
>>>>>>> [Feature #160577477] add test file for the feature
# Specify a namespace
app_name="authentication"

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view(), name='user-registration'),
    path('users/login/', LoginAPIView.as_view()),
<<<<<<< HEAD
    path('users/email_sent', EmailSentAPIView.as_view(), name='email_password'),
    path('users/password_reset', PasswordResetAPIView.as_view(), name='password_reset'),
=======
    path('users/email_sent', EmailSentAPIView.as_view()),
    path('users/password_reset', PasswordResetAPIView.as_view()),
>>>>>>> [Feature #160577477]users can receive links via  emails to reset password
]
