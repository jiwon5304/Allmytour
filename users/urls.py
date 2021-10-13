from django.urls import path
from users.views import LoginView, SignUpView, SearchPasswordView

urlpatterns = [
    path("/login", LoginView.as_view()),
    path("/signup", SignUpView.as_view()),
    path("/searchpw", SearchPasswordView.as_view()),
]
