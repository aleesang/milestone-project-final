from django.urls import path
from .views import customOrderView, successView

urlpatterns = [
    path('customorder/', customOrderView, name='customorder'),
    path('success/', successView, name='success'),
]