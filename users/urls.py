from django.urls import path
from users.views import LoginView, SignUpView, DoubleCheckEmailView

urlpatterns = [
    path("/login", LoginView.as_view()),
    path("/signup", SignUpView.as_view()),
    path("/signup/email/deplicate", DoubleCheckEmailView.as_view()),
]
