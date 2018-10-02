from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, EmailSentAPIView, PasswordResetAPIView
)
<<<<<<< HEAD

# Specify a namespace
app_name="authentication"

=======
>>>>>>> [Feature #160577477]users can receive links via  emails to reset password
urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view(), name='user-registration'),
    path('users/login/', LoginAPIView.as_view()),
    path('users/email_sent', EmailSentAPIView.as_view()),
    path('users/password_reset', PasswordResetAPIView.as_view()),
]
