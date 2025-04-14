from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # ✅ Enables the admin panel
    path('api/ipos/', include('ipo_tracker.urls')),  # Handles IPO-related endpoints
    path('api/', include('subscriptions.urls')),     # Handles subscriptions
]

