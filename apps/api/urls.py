from django.urls import path

from apps.api.views import ContactAPIView, GoogleSheetsProcessorViews

urlpatterns = [
    path("check/contact/", ContactAPIView.as_view()),
    path("gs/changed/", GoogleSheetsProcessorViews.as_view()),
]
