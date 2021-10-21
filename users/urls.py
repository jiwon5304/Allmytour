from django.urls import path
from users.views import (
    LoginView,
    SignUpView,
    SendEmailView,
    AuthenticationView,
    NewPasswordView,
)

urlpatterns = [
    path("/login", LoginView.as_view()),
    path("/signup", SignUpView.as_view()),
    path("/sendemail", SendEmailView.as_view()),
    path("/auth", AuthenticationView.as_view()),
    path("/newpw", NewPasswordView.as_view()),
]
