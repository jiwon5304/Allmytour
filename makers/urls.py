from django.urls import path

from makers.views import MakerReviseView
from makers.views import MakerApplyView, DraftMakerView

urlpatterns = [
    path("/apply", MakerApplyView.as_view()),
    path("/draft", DraftMakerView.as_view()),
    path("/revise", MakerReviseView.as_view()),
]
