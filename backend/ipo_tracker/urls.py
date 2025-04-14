from django.urls import path
from .views import get_upcoming_ipos

urlpatterns = [
    path('', get_upcoming_ipos),
]
