from django.urls import path
from .import views

urlpatterns=[
    path('map',views.map,name='map'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('process', views.process, name='process'),
    path('logout', views.logout, name='logout'),
    path('driverLogin', views.driverLogin, name='driverLogin'),
    path('driverRegister', views.driverRegister, name='driverRegister'),
    path('driverIndex', views.driverIndex, name='driverIndex'),
]