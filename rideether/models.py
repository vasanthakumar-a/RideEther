from django.db import models
from toolz.itertoolz import last

class driverDB(models.Model):
    driver_name = models.CharField(max_length=100)
    vehical_name = models.CharField(max_length=100)
    vehical_number = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    driver_address = models.CharField(max_length=100)

class waitingDB(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    drv_username = models.CharField(max_length=50)

class acceptDB(models.Model):
    driver_address = models.CharField(max_length=50)
    user_address = models.CharField(max_length=50)
    accept = models.CharField(max_length=50)