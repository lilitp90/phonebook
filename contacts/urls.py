from django.urls import path
from .views import ContactUploadView


urlpatterns = [
    path('', ContactUploadView.as_view(), name='upload'),
]