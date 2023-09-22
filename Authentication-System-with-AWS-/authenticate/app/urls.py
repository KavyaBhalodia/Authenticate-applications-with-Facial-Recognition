from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('', views.login, name='login'),

    path('success/', views.success, name='success'),
    path('error/', views.error, name='error')


    
]