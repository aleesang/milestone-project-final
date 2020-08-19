from django.urls import path
from . import views
from .views import checkout, checkout_success

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('order_success', views.order_success, name='order_success'),
]