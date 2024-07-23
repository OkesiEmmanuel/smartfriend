# myapp/urls.py

from django.urls import path
from .views import TutorView

urlpatterns = [
    path('tutor/', TutorView.as_view(), name='tutor'),
]