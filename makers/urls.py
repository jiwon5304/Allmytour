from django.urls import path

from makers.views import MakerReviseView

urlpatterns = [
    path("/revise", MakerReviseView.as_view()),
]
