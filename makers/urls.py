from django.urls import path

from makers.views import MakerApplyView

urlpatterns = [
    path("/apply", MakerApplyView.as_view()),
]
