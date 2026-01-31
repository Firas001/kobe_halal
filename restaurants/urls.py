from django.urls import path
from . import views

urlpatterns = [
    path('', views.restaurant_list, name='list'),
    path('restaurant/<int:pk>/', views.restaurant_detail, name='detail'),
]