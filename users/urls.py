from django.urls import path
from users.views import (
    LoginView,
    SignUpView,
    DoubleCheckEmailView,
    MypageView,
    PhoneCertificationView,
)

urlpatterns = [
    path("", MypageView.as_view()),
    path("/login", LoginView.as_view()),
    path("/signup", SignUpView.as_view()),
    path("/signup/email/deplicate", DoubleCheckEmailView.as_view()),
    path("/signup/phone/match", PhoneCertificationView.as_view()),
]
