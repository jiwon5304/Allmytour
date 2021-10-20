from django.urls import path

from makers.views import MakerApplyView, MakerApplyDraftView

urlpatterns = [
    path("/apply", MakerApplyView.as_view()),
    path("/draft", MakerApplyDraftView.as_view()),
]
