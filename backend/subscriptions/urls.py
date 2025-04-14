from django.urls import path
from .views import subscribe_user, unsubscribe_user

urlpatterns = [
    path('subscribe/', subscribe_user, name='subscribe_user'),
    path('unsubscribe/', unsubscribe_user, name='unsubscribe_user'),
]
