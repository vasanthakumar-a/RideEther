from django.urls import path
from .import views

urlpatterns=[
    path('',views.home,name='home'),
    path('map',views.map,name='map'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('process', views.process, name='process'),
    path('logout', views.logout, name='logout'),
    path('driverLogout', views.driverLogout, name='driverLogout'),
    path('driverLogin', views.driverLogin, name='driverLogin'),
    path('driverRegister', views.driverRegister, name='driverRegister'),
    path('driverIndex', views.driverIndex, name='driverIndex'),
    path('start', views.start, name='start'),
    path('stop', views.stop, name='stop'),
    path('transact', views.transact, name='transact'),
]