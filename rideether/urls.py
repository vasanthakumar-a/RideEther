from django.urls import path
from .import views

urlpatterns=[
    path('map',views.map,name='map'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('process', views.process, name='process'),
]