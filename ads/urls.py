from django.urls import path
from . import views

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('ad/new/', views.ad_create, name='ad_create'),
    path('ad/<int:pk>/edit/', views.ad_edit, name='ad_edit'),
    path('ad/<int:pk>/delete/', views.ad_delete, name='ad_delete'),
    path('my/', views.my_ads, name='my_ads'),
    path('register/', views.register, name='register'),
]
