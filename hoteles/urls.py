from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('reservar/<int:hotel_id>/', views.reservar, name='reservar'),
]
