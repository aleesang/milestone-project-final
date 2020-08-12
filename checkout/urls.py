from django.urls import path
from . import views
from .views import checkout, checkout_success

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success', views.checkout_success, name='checkout_success'),
]