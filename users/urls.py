from django.urls import path
from users.views import SigninView, SignUpView

urlpatterns = [
    path("/signin", SigninView.as_view()),
    path("/sign-up", SignUpView.as_view()),
]
